import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from common.utility import get_project_root
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl


class Card:
    __imagePath = None
    def __init__(self, local_translation=(0, 0), scale=1):
        self.tool_card = None
        self.pickable_card_base = None
        self.local_translation = local_translation
        self.scale = scale
        self.card_number = None


    def get_card_number(self):
        return self.card_number
        
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_card_base(self):
        return self.pickable_card_base

    def get_tool_card(self):
        return self.tool_card


    def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
        attached_tool_card = Rectangle(color=color,
                                       local_translation=local_translation,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        return attached_tool_card

    def create_card_base_pickable_rectangle(self, color, vertices, local_translation):
        pickable_card_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)
        pickable_card_base.set_draw_gradient(True)
        return pickable_card_base

    def create_illustration(self, image_path, vertices, local_translation):
        card_illustration = ImageRectangleElement(image_path=image_path,
                                                  local_translation=local_translation,
                                                  vertices=vertices)
        return card_illustration

    def create_equipped_mark(self, image_path, vertices, local_translation):
        card_equipped_mark = ImageRectangleElement(image_path=image_path,
                                                   local_translation=local_translation,
                                                   vertices=vertices)
        card_equipped_mark.set_visible(False)
        return card_equipped_mark


    def init_card(self, card_number):
        self.card_number = card_number
        project_root = get_project_root()

        cardInfo = CardInfoFromCsvRepositoryImpl.getInstance()
        csvInfo = cardInfo.readCardData(os.path.join(project_root, 'local_storage', 'card', 'data.csv'))
        cardInfo.build_dictionaries(csvInfo)

        CardControllerImpl()
        card_controller = CardControllerImpl.getInstance()

        self.tool_card = self.create_attached_tool_card_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            local_translation=self.local_translation,
            vertices=[(20, 20), (370, 20), (370, 520), (20, 520)])

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=[(0, 0), (350, 0), (350, 500), (0, 500)]
            )
        )



        self.pickable_card_base.set_attached_shapes(
            self.create_illustration(
                image_path=os.path.join(project_root, "local_storage", "card_images", f"{card_number}.png"),
                local_translation=self.local_translation,
                vertices=[(25, 25), (325, 25), (325, 325), (25, 325)]
            )
        )

        self.pickable_card_base.set_attached_shapes(
            self.create_equipped_mark(
                image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
                local_translation=self.local_translation,
                vertices=[(390, 30), (430, 30), (430, 70), (390, 70)]
            )
        )

        card_controller_shapes = card_controller.getCardTypeTable(cardInfo.getCardTypeDictionary(card_number))
        card_shapes = card_controller_shapes(self.local_translation)
        for shape in card_shapes:
            self.pickable_card_base.set_attached_shapes(shape)