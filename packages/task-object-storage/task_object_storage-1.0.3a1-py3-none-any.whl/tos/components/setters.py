import os
import platform
import warnings

from pymongo.collection import ReturnDocument

from tos.statuses import VALID_STATUSES
from tos.utils import accept_string_object_ids


class TaskSetters:

    def _update_task_object(self, filter: dict, update: dict, sort=None):
        """
        Base task object setter and update method.

        :param filter: MongoDB query
        :type filter: dict
        :param update: Update operation to apply
        :type update: dict
        :param sort: Order for the query if multiple matches
        :param sort: list
        :returns: Updated task object
        :rtype: dict
        """
        return self.tos.find_one_and_update(
            filter,
            update,
            projection=None,
            sort=sort,
            return_document=ReturnDocument.AFTER
        )

    def update_task_object_and_timestamp(self, filter: dict, update: dict, sort=None):
        """
        Update task object and the modification time.
        Do not use this method directly.

        :param filter: MongoDB query
        :type filter: dict
        :param update: Update operation to apply
        :type update: dict
        :param sort: Order for the query if multiple matches
        :param sort: list
        :returns: Updated task object
        :rtype: dict
        """
        if "$currentDate" in update:
            update["$currentDate"] = {
                    **update["$currentDate"],
                    "updatedAt": {"$type": "date"}
            }
        else:
            update = {
                **update,
                "$currentDate": {"updatedAt": {"$type": "date"}}
            }
        return self._update_task_object(
            filter,
            update,
            sort
        )

    @accept_string_object_ids
    def set_task_object_status(self, object_id, status):
        """
        Set the task object status to one of the accepted values.

        Accepted values are in :attr:`settings.VALID_STATUSES`

        :param object_id: Object id.
        :type object_id: str or ObjectId
        :param status: status text
        :type status: str
        :returns: Updated task object
        :rtype: dict
        """
        self._validate_status_text(status)
        return self._set_task_object_item(object_id, "status", status)

    def _validate_status_text(self, status):
        # TODO: use MongoDB schema validation instead of this
        if status not in VALID_STATUSES:
            raise ValueError("Trying to set invalid status")

    @accept_string_object_ids
    def set_task_object_stage(self, object_id, stage: int):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param stage: target stage
        :type stage: int

        :returns: Updated task object
        :rtype: dict
        """
        return self._set_task_object_item(object_id, "stage", stage)

    @accept_string_object_ids
    def set_task_object_payload(self, object_id, new_payload):
        """
        Replace the current payload object with an updated one.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param new_payload: new payload object
        :type new_payload: dict

        :returns: Updated task object
        :rtype: dict
        """
        return self._set_task_object_item(object_id, "payload", new_payload)

    @accept_string_object_ids
    def set_task_object_analytics(self, object_id, new_analytics):
        """
        Replace the current analytics object with an updated one.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param new_analytics: new analytics object
        :type new_analytics: dict

        :returns: Updated task object
        :rtype: dict
        """
        return self._set_task_object_item(object_id, "analytics", new_analytics)

    @accept_string_object_ids
    def set_task_object_last_error(self, object_id, error_text):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param error_text: Exception stacktrace or error text
        :type error_text: str

        :returns: Updated task object
        :rtype: dict
        """
        return self._set_task_object_item(object_id, "last_error", error_text)

    @accept_string_object_ids
    def set_task_object_analytics_item(self, object_id, key, value):
        """Update one item in the analytics dict.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: analytics item key
        :type key: str
        :param value: analytics item value
        :type value: str
        :returns: Updated task object
        :rtype: dict
        """
        item_name = f"analytics.{key}"
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {item_name: value}}
        )

    @accept_string_object_ids
    def set_task_object_priority(self, object_id, new_priority):
        """Set the priority of a task object.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param new_priority: New desired priority
        :type new_priority: int
        :returns: Updated task object
        :rtype: dict
        """
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {"priority": new_priority}}
        )

    @accept_string_object_ids
    def _set_task_object_item(self, object_id, field_name, new_item):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param field_name: name of the field to set
        :type field_name: str
        :param new_item: new value of the field
        :type new_item: str

        :returns: Updated task object
        :rtype: dict
        """
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {field_name: new_item}}
        )

    @accept_string_object_ids
    def set_task_object_to_manual_handling(self, object_id):
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {"manual": True}}
        )

    @accept_string_object_ids
    def set_task_object_for_rerun(self, object_id):
        """
        Decrement stage and set status to pass for rerunning the
        previous stage.

        :param object_id: Object id
        :type object_id: str or ObjectId

        :raises ValueError: if current task object stage is 0 or less
        :returns: Updated task object
        :rtype: dict
        """

        task_object = self.find_task_object_by_id(object_id)
        if task_object["stage"] <= 0:
            raise ValueError("Cannot decrement stage to negative number")

        self.increment_retry_count(object_id)
        self.decrement_task_object_stage(object_id)
        return self.set_task_object_status(object_id, "pass")

    def set_task_object_executor(self, object_id):
        text = self._get_executor_info()
        return self._set_task_object_item(object_id, "executor", text)

    def _get_executor_info(self):
        node_name = os.environ.get("NODE_NAME", platform.node())
        executor_number = os.environ.get("EXECUTOR_NUMBER", 1)
        return f"Executor {executor_number} on node {node_name}"

    def set_task_object_build_number(self, object_id):
        build_nr = os.environ.get("BUILD_NUMBER", None)
        return self._set_task_object_item(object_id, "build_number", build_nr)

    def set_task_object_job_name(self, object_id):
        job_name = os.environ.get("JOB_NAME", None)
        return self._set_task_object_item(object_id, "job_name", job_name)

    @accept_string_object_ids
    def set_stage_start_time(self, object_id, stage):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param stage: target stage
        :type stage: int

        :returns: Updated task object
        :rtype: dict
        """
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$currentDate": {
                f"stages.{stage}.startedAt": {"$type": "date"}
            }}
        )

    @accept_string_object_ids
    def set_stage_end_time(self, object_id, stage):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param stage: target stage
        :type stage: int

        :returns: Updated task object
        :rtype: dict
        """
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$currentDate": {
                f"stages.{stage}.endedAt": {"$type": "date"}
            }}
        )

    @accept_string_object_ids
    def set_stage_status(self, object_id, stage, status):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param stage: target stage
        :type stage: int

        :returns: Updated task object
        :rtype: dict
        """
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {f"stages.{stage}.status": status}}
        )

    @accept_string_object_ids
    def set_stage_build_number(self, object_id, stage):
        build_nr = os.environ.get("BUILD_NUMBER", None)
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {f"stages.{stage}.build_number": build_nr}}
        )

    @accept_string_object_ids
    def set_stage_executor(self, object_id, stage):
        executor = self._get_executor_info()
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {f"stages.{stage}.executor": executor}}
        )

    @accept_string_object_ids
    def set_retry_start_time(self, object_id, stage, retry_count):
        # TODO: should combine stage and retry object handling, they are mostly
        # duplicate code!
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$currentDate": {
                f"stages.{stage}.retries.{retry_count}.startedAt": {"$type": "date"}
            }}
        )

    @accept_string_object_ids
    def set_retry_end_time(self, object_id, stage, retry_count):
        # TODO: should combine stage and retry object handling, they are mostly
        # duplicate code!
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$currentDate": {
                f"stages.{stage}.retries.{retry_count}.endedAt": {"$type": "date"}
            }}
        )

    @accept_string_object_ids
    def set_retry_executor(self, object_id, stage, retry_count):
        # TODO: should combine stage and retry object handling, they are mostly
        # duplicate code!
        executor = self._get_executor_info()
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {f"stages.{stage}.retries.{retry_count}.executor": executor}}
        )

    @accept_string_object_ids
    def set_retry_build_number(self, object_id, stage, retry_count):
        # TODO: should combine stage and retry object handling, they are mostly
        # duplicate code!
        build_nr = os.environ.get("BUILD_NUMBER", None)
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {f"stages.{stage}.retries.{retry_count}.build_number": build_nr}}
        )
