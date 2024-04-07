from src.Utils import Utils
from src.mail import Mail
import unicodedata
import PyPDF2


class Content:

    def __init__(self, pdf_reader: PyPDF2.PdfReader):
        self.__pdfReader = pdf_reader
        self.__index_first_page = 0
        self.__pos_last_character_first_page = -1

        self.__load_text_attribut()

    def __load_text_attribut(self) -> None:
        """
        Charge le contenu du text dans les deux attributs

        :return: None
        """
        premiere_page = self.__pdfReader.pages[self.__index_first_page].extract_text()

        if premiere_page.startswith("This article") and not Mail.find_emails(premiere_page)[0]:
            self.__index_first_page += 1
            premiere_page = self.__pdfReader.pages[self.__index_first_page].extract_text()

        self.__pos_last_character_first_page = len(premiere_page) - 1

        self.__text = premiere_page + "".join(
            self.__pdfReader.pages[x].extract_text() for x in
            range(self.__index_first_page + 1, len(self.__pdfReader.pages)))

        self.__text = Utils.replace_accent(self.__text)

        # Filtre les caractères pour ne conserver que les caractères ASCII
        chaine_normalisee = unicodedata.normalize('NFD', self.__text.lower())

        self.__text_lower = ''.join(c for c in chaine_normalisee if unicodedata.category(c) != 'Mn')
        ######################################################################

        # Remplace le mot clef pour mieux le retrouver
        self.__text_lower = self.__text_lower.replace("cknowledgement", "cknowledgment ")
        ######################################################################

    def get_text(self) -> str:
        """
        Renvoi le texte du pdf

        :return: string content
        """
        return self.__text

    def get_text_lower(self) -> str:
        """
        Renvoi le contenu du pdf en minuscule sans accent

        :return: string content
        """
        return self.__text_lower

    def get_pos_last_character_first_page(self) -> int:
        """
        Renvoi la position du dernier caractère de la première page

        :return: int valeur
        """
        return self.__pos_last_character_first_page

    def get_index_first_page(self) -> int:
        """
        Renvoi l'indice de la première page

        :return: int valeur
        """
        return self.__index_first_page