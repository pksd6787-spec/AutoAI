from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Callable
from uuid import uuid4

from app.services.workflows.engine import WorkflowEngine


class RuntimeStatus(StrEnum):
    pending = "pending"
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    paused = "paused"
    canceled = "canceled"
    retrying = "retrying"


@dataclass
class RuntimeJob:
    id: str
    workflow_id: str
    job_type: str
    status: RuntimeStatus = RuntimeStatus.pending
    parallel: bool = False
    attempts: int = 0
    max_attempts: int = 3
    input: dict = field(default_factory=dict)
    output: dict = field(default_factory=dict)
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class RuntimeWorkflow:
    id: str
    project_id: str
    workflow_type: str
    status: RuntimeStatus = RuntimeStatus.pending
    input: dict = field(default_factory=dict)
    output: dict = field(default_factory=dict)
    jobs: list[RuntimeJob] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None


class WorkflowRuntime:
    """Small durable-state-compatible workflow runtime.

    The class is intentionally storage-agnostic for Phase 3. API code can use the
    in-memory repository today, while the same state transitions map directly to
    PostgreSQL `workflows` and `jobs` rows from the migrations.
    """

    def __init__(self, job_handlers: dict[str, Callable[[dict], dict]] | None = None):
        self.workflows: dict[str, RuntimeWorkflow] = {}
        self.queue: list[str] = []
        self.job_handlers = job_handlers or {}

    def create_daily_workflow(self, project_id: str, workflow_input: dict | None = None) -> RuntimeWorkflow:
        workflow = RuntimeWorkflow(
            id=str(uuid4()),
            project_id=project_id,
            workflow_type="daily_documentary",
            input=workflow_input or {},
        )
        for planned in WorkflowEngine().plan_daily_documentary(project_id):
            workflow.jobs.append(RuntimeJob(
                id=str(uuid4()),
                workflow_id=workflow.id,
                job_type=planned["job_type"],
                parallel=planned.get("parallel", False),
                input=workflow.input,
            ))
        self.workflows[workflow.id] = workflow
        return workflow

    def enqueue(self, workflow_id: str) -> RuntimeWorkflow:
        workflow = self._get(workflow_id)
        if workflow.status in {RuntimeStatus.canceled, RuntimeStatus.completed}:
            return workflow
        workflow.status = RuntimeStatus.queued
        for job in workflow.jobs:
            if job.status == RuntimeStatus.pending:
                job.status = RuntimeStatus.queued
        if workflow_id not in self.queue:
            self.queue.append(workflow_id)
        return workflow

    def pause(self, workflow_id: str) -> RuntimeWorkflow:
        workflow = self._get(workflow_id)
        workflow.status = RuntimeStatus.paused
        return workflow

    def resume(self, workflow_id: str) -> RuntimeWorkflow:
        workflow = self._get(workflow_id)
        if workflow.status == RuntimeStatus.paused:
            workflow.status = RuntimeStatus.queued
            if workflow_id not in self.queue:
                self.queue.append(workflow_id)
        return workflow

    def cancel(self, workflow_id: str) -> RuntimeWorkflow:
        workflow = self._get(workflow_id)
        workflow.status = RuntimeStatus.canceled
        for job in workflow.jobs:
            if job.status in {RuntimeStatus.pending, RuntimeStatus.queued, RuntimeStatus.retrying}:
                job.status = RuntimeStatus.canceled
        if workflow_id in self.queue:
            self.queue.remove(workflow_id)
        return workflow

    def run_next(self) -> RuntimeWorkflow | None:
        if not self.queue:
            return None
        workflow_id = self.queue.pop(0)
        workflow = self._get(workflow_id)
        if workflow.status in {RuntimeStatus.paused, RuntimeStatus.canceled, RuntimeStatus.completed}:
            return workflow
        workflow.status = RuntimeStatus.running
        workflow.started_at = workflow.started_at or datetime.now(timezone.utc)
        for job in workflow.jobs:
            if job.status not in {RuntimeStatus.queued, RuntimeStatus.retrying}:
                continue
            self._run_job(job)
            if job.status == RuntimeStatus.failed:
                workflow.status = RuntimeStatus.failed
                workflow.output["failed_job_id"] = job.id
                workflow.output["error_message"] = job.error_message
                return workflow
        workflow.status = RuntimeStatus.completed
        workflow.completed_at = datetime.now(timezone.utc)
        workflow.output["completed_jobs"] = len(workflow.jobs)
        return workflow

    def _run_job(self, job: RuntimeJob) -> None:
        job.status = RuntimeStatus.running
        job.started_at = datetime.now(timezone.utc)
        job.attempts += 1
        try:
            handler = self.job_handlers.get(job.job_type, self._default_handler)
            job.output = handler(job.input | {"job_type": job.job_type})
            job.status = RuntimeStatus.completed
            job.completed_at = datetime.now(timezone.utc)
        except Exception as exc:
            job.error_message = str(exc)
            job.status = RuntimeStatus.retrying if job.attempts < job.max_attempts else RuntimeStatus.failed
            if job.status == RuntimeStatus.retrying:
                job.status = RuntimeStatus.queued

    def _default_handler(self, payload: dict) -> dict:
        return {"status": "planned", "job_type": payload["job_type"]}

    def _get(self, workflow_id: str) -> RuntimeWorkflow:
        if workflow_id not in self.workflows:
            raise KeyError(f"Workflow {workflow_id} not found")
        return self.workflows[workflow_id]


runtime = WorkflowRuntime()
