from bson.binary import Binary
from pymongo.collection import ReturnDocument

from tos.utils import accept_string_object_ids


class TaskUpdaters:

    def _update_task_object(self, filter: dict, update: dict, sort=None):
        """
        Base task object setter and update method.

        :param filter: MongoDB query
        :type filter: dict
        :param update: Update operation to apply
        :type update: dict
        :param sort: Order for the query if multiple matches
        :type sort: list
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
        Update task object and the modification time. Do not call this method directly.

        :param filter: MongoDB query
        :type filter: dict
        :param update: Update operation to apply
        :type update: dict
        :param sort: Order for the query if multiple matches
        :type sort: list
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
    def increment_retry_count(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: Updated task object
        :rtype: dict
        """
        # TODO: move to setters
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$inc": {"retry_count": 1}}
        )

    @accept_string_object_ids
    def increment_task_object_stage(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: Updated task object
        :rtype: dict
        """
        # TODO: move to setters
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$inc": {"stage": 1}}
        )

    @accept_string_object_ids
    def decrement_task_object_stage(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: Updated task object
        :rtype: dict
        """
        # TODO: move to setters
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$inc": {"stage": -1}}
        )

    @accept_string_object_ids
    def add_binary_data_to_payload(self, object_id, filepath, data_title):
        """
        Put an encoded binary string to database.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param filepath: file path to the file to encode
        :type filepath: str
        :param data_title: name of the binary data to store.
        :type data_title: str

        :returns: Updated task object
        :rtype: dict

        :ivar bin_data: bson.Binary encoded binary data
        """
        bin_data = self._encode_binary_data(filepath)
        return self.add_key_value_pair_to_payload(object_id, data_title, bin_data)

    def _encode_binary_data(self, filepath):
        """
        Encode a file to a binary string presentation.

        :param filepath: file path to the file to encode
        :type filepath: str

        :returns: encoded file
        :rtype: bson.Binary
        """
        with open(filepath, "rb") as f:
            encoded = Binary(f.read())
        return encoded

    @accept_string_object_ids
    def update_payload(self, object_id, update):
        """
        Update task object payload with new data.
        Note that only updates top level of payload - nested documents will be overwritten!

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param update: key-value pair(s) to add to payload
        :type update: dict

        :raises TypeError: when ``update`` is not a dict.
        :returns: Updated task object
        :rtype: dict
        """
        if not isinstance(update, dict):
            raise TypeError("Argument update should be a dict")

        update = {f"payload.{key}": value for key, value in update.items()}
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": update}
        )

    @accept_string_object_ids
    def add_key_value_pair_to_payload(self, object_id, key, value):
        """
        Add single key-value pair to payload.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: name of the field to insert
        :type key: str
        :param value: value of the field to insert
        :type value: str

        :returns: Updated task object
        :rtype: dict
        """
        item_name = f"payload.{key}"
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$set": {item_name: value}}
        )

    @accept_string_object_ids
    def remove_field_from_payload(self, object_id, key):
        """
        Remove single key-value pair from payload.
        A nested key-value pair can be removed by referring to it with dot notation.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: name of the field to remove
        :type key: str

        :returns: Updated task object
        :rtype: dict
        """
        item_name = f"payload.{key}"
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$unset": {item_name: ""}}
        )

    @accept_string_object_ids
    def push_value_to_array_field(self, object_id, value, field_name):
        """
        Push an arbitrary value to an array type field.

        Push is an upsert operation; if the array doesn't exist,
        it will be created.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param value: value of the field to insert
        :type value: str, int or dict
        :param field_name: Name of the array field, e.g. 'analytics' or
            'payload.alerts'
        :type field_name: str

        :returns: Updated task object
        :rtype: dict
        """
        return self.update_task_object_and_timestamp(
            {"_id": object_id},
            {"$push": {field_name: value}}
        )

    @accept_string_object_ids
    def update_stage_exceptions(self, object_id, error_text, stage):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param error_text: Exception stacktrace or error text
        :type error_text: str

        :returns: Updated task object
        :rtype: dict
        """
        return self.push_value_to_array_field(
            object_id,
            error_text,
            f"stages.{stage}.exceptions"
        )

    @accept_string_object_ids
    def update_stage_retry_count(self, object_id, stage):
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
            {"$inc": {f"stages.{stage}.retry_count": 1}}
        )

    def update_stage_object(self, object_id, current_stage):
        """Update stages object with new stage."""
        self.set_task_object_stage(object_id, current_stage)
        self.set_stage_start_time(object_id, current_stage)
        self.set_stage_build_number(object_id, current_stage)
        self.set_stage_executor(object_id, current_stage)

    def update_status(self, object_id, current_stage, status):
        """Update task object and its stages object with new status."""
        self.set_task_object_status(object_id, status)
        self.set_stage_status(object_id, current_stage, status)

    def update_exceptions(self, object_id, current_stage, error_text):
        """Update task object and its stages object with the new exception."""
        self.set_task_object_last_error(object_id, error_text)
        self.update_stage_exceptions(object_id, error_text, current_stage)

    def save_retry_metadata_if_retry(self, to, current_stage):
        """
        For every run, check if it's a retry.
        If it is, populate a retry object inside the stage object.
        This way we get to know when and where the job has been running
        on failures.
        """
        # TODO: combine this with update_stage, they are mostly duplicate code
        if to.get("retry_count", 0) > 0:
            self._update_retries_data(
                to["_id"],
                current_stage,
                to["retry_count"]
            )

    def _update_retries_data(self, object_id, current_stage, retry_count):
        self.set_retry_build_number(object_id, current_stage, retry_count)
        self.set_retry_executor(object_id, current_stage, retry_count)
