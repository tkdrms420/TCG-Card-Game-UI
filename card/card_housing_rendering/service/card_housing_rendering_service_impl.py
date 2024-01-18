import tkinter

from card.card_housing_rendering.repository.card_housing_rendering_repository_impl import \
    CardHousingRenderingRepositoryImpl
from card.card_housing_rendering.service.card_housing_rendering_service import CardHousingRenderingService


class CardHousingRenderingServiceImpl(CardHousingRenderingService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardFrameRepository = CardHousingRenderingRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardHousingUiRendering(self, rootWindow, switchFrameWithMenuName):
        CardFrame = self.__cardFrameRepository.createCardFrame(rootWindow)

        label_text = "My Card"
        label = tkinter.Label(CardFrame, text=label_text, font=("Helvetica", 20), bg="#AE905E", fg="black",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")

        deck_generation_button = tkinter.Button(CardFrame, text="이전 페이지", bg="#2E7D32", fg="white",
                                      command=lambda: switchFrameWithMenuName("lobby-menu"), width=24, height=2)
        deck_generation_button.place(relx=0.3, rely=0.9, anchor="e")

        go_back_to_lobby_button = tkinter.Button(CardFrame, text="다음 페이지", bg="#C62828", fg="white",
                                     command=lambda: switchFrameWithMenuName("lobby-menu"), width=24, height=2)
        go_back_to_lobby_button.place(relx=0.7, rely=0.9, anchor="w")


        return CardFrame