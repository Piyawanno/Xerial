from xerial.input.TextInput import TextInput
from xerial.input.TextAreaInput import TextAreaInput
from xerial.input.LabelInput import LabelInput
from xerial.input.EnableInput import EnableInput
from xerial.input.PasswordInput import PasswordInput
from xerial.input.HiddenInput import HiddenInput
from xerial.input.NumberInput import NumberInput
from xerial.input.FileInput import FileInput
from xerial.input.FileMatrixInput import FileMatrixInput
from xerial.input.EmailInput import EmailInput
from xerial.input.DateTimeInput import DateTimeInput
from xerial.input.DateInput import DateInput
from xerial.input.TimeInput import TimeInput
from xerial.input.TimeSpanInput import TimeSpanInput
from xerial.input.ColorInput import ColorInput
from xerial.input.EnumCheckBoxInput import EnumCheckBoxInput
from xerial.input.EnumRadioInput import EnumRadioInput
from xerial.input.EnumSelectInput import EnumSelectInput
from xerial.input.ReferenceCheckBoxInput import ReferenceCheckBoxInput
from xerial.input.ReferenceRadioInput import ReferenceRadioInput
from xerial.input.ReferenceSelectInput import ReferenceSelectInput
from xerial.input.AutoCompleteInput import AutoCompleteInput

from enum import IntEnum

class InputType (IntEnum) :
	TEXT = 10
	TEXT_AREA = 11
	LABEL = 12
	ENABLE = 13
	PASSWORD = 14
	HIDDEN = 15
	NUMBER = 16
	FILE = 17
	FILE_MATRIX = 18
	EMAIL = 19
	DATE_TIME = 20
	DATE = 21
	TIME = 22
	TIME_SPAN = 23
	COLOR = 24
	ENUM_CHECKBOX  = 30
	ENUM_RADIO = 31
	ENUM_SELECT = 32
	REFERENCE_CHECKBOX = 33
	REFERENCE_RADIO = 34
	REFERENCE_SELECT = 35
	AUTOCOMPLETE = 36

InputType.mapped = {
	InputType.TEXT: TextInput,
	InputType.TEXT_AREA: TextAreaInput,
	InputType.LABEL: LabelInput,
	InputType.ENABLE: EnableInput,
	InputType.PASSWORD: PasswordInput,
	InputType.HIDDEN: HiddenInput,
	InputType.NUMBER: NumberInput,
	InputType.FILE: FileInput,
	InputType.FILE_MATRIX: FileMatrixInput,
	InputType.EMAIL: EmailInput,
	InputType.DATE_TIME: DateTimeInput,
	InputType.DATE: DateInput,
	InputType.TIME: TimeInput,
	InputType.TIME_SPAN : TimeSpanInput,
	InputType.COLOR: ColorInput,
	InputType.ENUM_CHECKBOX: EnumCheckBoxInput,
	InputType.ENUM_RADIO: EnumRadioInput,
	InputType.ENUM_SELECT: EnumSelectInput,
	InputType.REFERENCE_CHECKBOX: ReferenceCheckBoxInput,
	InputType.REFERENCE_RADIO: ReferenceRadioInput,
	InputType.REFERENCE_SELECT: ReferenceSelectInput,
	InputType.AUTOCOMPLETE: AutoCompleteInput,
}