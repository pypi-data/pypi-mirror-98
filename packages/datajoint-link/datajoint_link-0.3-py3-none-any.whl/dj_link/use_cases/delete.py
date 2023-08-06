"""Contains code pertaining to the delete use-case."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Set, Tuple

from .base import AbstractRequestModel, AbstractResponseModel, AbstractUseCase

if TYPE_CHECKING:
    from . import RepositoryLink


@dataclass
class DeleteRequestModel(AbstractRequestModel):
    """Request model for the delete use-case."""

    identifiers: List[str]


@dataclass
class DeleteResponseModel(AbstractResponseModel):
    """Response model for the delete use-case."""

    requested: Set[str]
    deletion_approved: Set[str]
    deleted_from_outbound: Set[str]
    deleted_from_local: Set[str]

    @property
    def n_requested(self):
        """Return the number of entities whose deletion was requested."""
        return len(self.requested)

    @property
    def n_deletion_approved(self):
        """Return the number of entities whose deletion was approved."""
        return len(self.deletion_approved)

    @property
    def n_deleted_from_outbound(self):
        """Return the number of entities who were deleted from the outbound table."""
        return len(self.deleted_from_outbound)

    @property
    def n_deleted_from_local(self):
        """Return the number od entities who were deleted from the local table."""
        return len(self.deleted_from_local)


class DeleteUseCase(
    AbstractUseCase[DeleteRequestModel]
):  # pylint: disable=unsubscriptable-object,too-few-public-methods
    """Use-case that deletes entities from the local table and executes associated logic."""

    response_model_cls = DeleteResponseModel

    def execute(self, repo_link: RepositoryLink, request_model: DeleteRequestModel) -> DeleteResponseModel:
        """Execute logic associated with the deletion of entities from the local repository."""
        deletion_requested, deletion_not_requested = self._group_by_deletion_requested(
            repo_link, request_model.identifiers
        )
        self._approve_deletion(repo_link, deletion_requested)
        self._delete_from_outbound(repo_link, deletion_not_requested)
        self._delete_from_local(repo_link, request_model.identifiers)
        # noinspection PyArgumentList
        return self.response_model_cls(
            requested=set(request_model.identifiers),
            deletion_approved=deletion_requested,
            deleted_from_outbound=deletion_not_requested,
            deleted_from_local=set(request_model.identifiers),
        )

    @staticmethod
    def _group_by_deletion_requested(repo_link: RepositoryLink, identifiers: List[str]) -> Tuple[Set[str], Set[str]]:
        deletion_requested = {i for i in identifiers if repo_link.outbound.flags[i]["deletion_requested"]}
        deletion_not_requested = set(identifiers) - deletion_requested
        return deletion_requested, deletion_not_requested

    @staticmethod
    def _approve_deletion(repo_link: RepositoryLink, deletion_requested: Set[str]) -> None:
        for identifier in deletion_requested:
            repo_link.outbound.flags[identifier]["deletion_approved"] = True

    @staticmethod
    def _delete_from_outbound(repo_link: RepositoryLink, deletion_not_requested: Set[str]) -> None:
        for identifier in deletion_not_requested:
            del repo_link.outbound[identifier]

    @staticmethod
    def _delete_from_local(repo_link: RepositoryLink, identifiers: List[str]) -> None:
        for identifier in identifiers:
            del repo_link.local[identifier]
