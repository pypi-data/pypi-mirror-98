from datetime import datetime
from typing import List
from google.cloud import firestore
from xialib.ager import Ager

class FirestoreAger(Ager):
    """Ager By Using Firestore database


    """
    def __init__(self, collection: str, db: firestore.Client):
        super().__init__()
        if not isinstance(db, firestore.Client):
            self.logger.error("FirestoreDepositor db must be type of Firestore Client", extra=self.log_context)
            raise TypeError("XIA-010003")
        else:
            self.db = db
            self.collection = db.collection(collection)


    @classmethod
    def age_list_add_item(cls, age_list: List[list], item: list) -> List[list]:
        new_age_list, cur_item, start_point = list(), item.copy(), None
        for list_item in age_list:
            # <List Item> --- <New Item>
            if list_item[1] + 1 < cur_item[0]:
                new_age_list.append(list_item)
            # <New Item> --- <List Item>
            elif cur_item[1] + 1 < list_item[0]:
                new_age_list.append(cur_item)
                cur_item = list_item.copy()
            # <New Item && List Item>
            else:
                cur_item = [min(cur_item[0], list_item[0]), max(cur_item[1], list_item[1])]
        new_age_list.append(cur_item)
        return new_age_list

    def key_init(self, key: str, start_key: int):
        ager_ref = self.collection.document(key).get()
        ager_ref.reference.set({datetime.now().strftime("%Y%m%d%H%M%S"): [str(start_key) + "-" + str(start_key)]})

    def get_ready_age(self, key: str, start_key: int, end_key: int) -> int:
        """Adding age range and get the last ready age

        Attributes:
            key (:obj:`str`): object key (key should contains Target Topic, Target Table, Segment ID)
            start_key (:obj:`int`): new input start merge key
            end_key (:obj:`int`): new input end merge key

        Return:
            :obj:`int`: The end age number which is ready to be loaded (No GAP from beginning)
        """
        ager_ref = self.collection.document(key).get()
        if not ager_ref.exists:
            raise ValueError("Target {} has not been initialized".format(key))
        ager_dict = ager_ref.to_dict()
        current_frame_id = datetime.now().strftime("%Y%m%d%H%M%S")
        current_frame_list = ager_dict.get(current_frame_id, [])
        current_frame_list.append(str(start_key) + "-" + str(end_key))
        ager_dict[current_frame_id] = current_frame_list

        all_list, last_ok_frame = [], ""
        for frame_id in sorted(ager_dict):
            for item in ager_dict[frame_id]:
                all_list = self.age_list_add_item(all_list, [int(item.split("-")[0]), int(item.split("-")[1])])

        for frame_id in sorted(ager_dict):
            if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                last_ok_frame = frame_id
        update_task = {current_frame_id: firestore.ArrayUnion([str(start_key) + "-" + str(end_key)])}
        # last_ok_frame could be empty if the ok frame contains gap
        if last_ok_frame:
            update_task[last_ok_frame] = firestore.ArrayUnion([str(all_list[0][0]) + "-" + str(all_list[0][-1])])
            for frame_id in [id for id in sorted(ager_dict) if id < last_ok_frame]:
                if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                    update_task[frame_id] = firestore.DELETE_FIELD
        # Incremental Updates
        ager_ref.reference.update(update_task)
        return all_list[0][-1]
