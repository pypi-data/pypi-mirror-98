from .utils import parse_date, parse_datetime


class ResultSet(list):
    pass


class Entity:

    result_set_class = ResultSet

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        return pickle

    def __getattr__(self, name):
        """
        invoken when refering to attribute that it is not valid or it was not present at json response
        """
        return None

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into an entity instance."""
        instance = cls()
        for k, v in json.items():
            if hasattr(cls, 'extra_parsers') and k in cls.extra_parsers:
                func = cls.extra_parsers[k]
                setattr(instance, k, func(v))
            else:
                setattr(instance, k, v)
        return instance

    @classmethod
    def parse_list(cls, json):
        results = cls.result_set_class()
        total = 0
        items = json or []
        for obj in items:
            results.append(cls.parse(obj))
            total += 1
        # hold the count of items
        results.total = total
        return results


class ElectionProcessResultSet(ResultSet):

    @property
    def exclude_empty_item(self):
        return [item for item in self if item.idProcesoElectoral != 0]


class ElectionProcess(Entity):

    result_set_class = ElectionProcessResultSet
    extra_parsers = {
        'strFechaAperturaProceso': parse_date,
        'strFechaConvocatoria': parse_date,
        'strFechaCierreProceso': parse_date,
        'strFechaRegistro': lambda v: parse_datetime(
            v, format="%d/%m/%Y %H:%M:%S %p"),
    }


class ElectionType(Entity):
    pass


class ElectoralDistrict(Entity):
    pass


class Candidate(Entity):

    extra_parsers = {
        'strFechaNacimiento': lambda v: parse_datetime(
            v, format="%d/%m/%Y %H:%M:%S %p"),
    }
    pass


class ProceduralPart(Entity):
    pass


class Document(Entity):
    pass


class File(Entity):

    extra_parsers = {
        'lParteProcesal': ProceduralPart.parse_list
    }


class FileExtended(Entity):

    extra_parsers = {
        'oExpediente': File.parse,
        'lReporteBusquedaExpediente': Document.parse_list,  # documents
        'lCandidatosExpediente': Candidate.parse_list,  # candidates
        'lAsociadosPadre': File.parse_list,  # files related directly
        'lAsociadosHijos': File.parse_list,  # other files related (procedural part)
    }


class MovableProperty(Entity):
    pass


class ImmovableProperty(Entity):
    pass


class BasicEducation(Entity):
    pass


class PartisanPosition(Entity):
    pass


class UniversityEducation(Entity):
    pass


class NonUniversityEducation(Entity):
    pass


class PostgraduateEducation(Entity):
    pass


class TechnicalEducation(Entity):
    pass


class ProfessionalExperience(Entity):
    pass


class ResignationPoliticalOrganization(Entity):
    pass


class ObligationSentence(Entity):
    pass


class PenalSentence(Entity):
    pass


class PersonalInfo(Entity):

    extra_parsers = {
        'strFeTerminoRegistro': parse_datetime,
        'strFechaNacimiento': parse_date
    }


class AdditionalInformation(Entity):
    pass


class Income(Entity):
    pass


class Resume(Entity):

    extra_parsers = {
        'lBienInmueble': ImmovableProperty.parse_list,
        'lBienMueble': MovableProperty.parse_list,
        'lCargoPartidario': PartisanPosition.parse_list,
        'lEduUniversitaria': UniversityEducation.parse_list,
        'lExperienciaLaboral': ProfessionalExperience.parse_list,
        'lRenunciaOP': ResignationPoliticalOrganization.parse_list,
        'lSentenciaObliga': ObligationSentence.parse_list,
        'lSentenciaPenal': PenalSentence.parse_list,
        'oDatosPersonales': PersonalInfo.parse,
        'oEduBasica': BasicEducation.parse,
        'oEduNoUniversitaria': NonUniversityEducation.parse,
        'oEduPosgrago': PostgraduateEducation.parse,
        'oEduTecnico': TechnicalEducation.parse,
        'oInfoAdicional': AdditionalInformation.parse,
        'oIngresos': Income.parse,
    }


class EntityFactory:
    election_process = ElectionProcess
    election_type = ElectionType
    electoral_district = ElectoralDistrict
    file = File
    file_extended = FileExtended
    candidate = Candidate
    resume = Resume
