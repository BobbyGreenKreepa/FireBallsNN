import cachetools
from fireballsnn_api import serializers
from fireballsnn_api import models
from nuro_link_algo import neuro_link


class CourtNameService:
    cache = cachetools.LRUCache(maxsize=1000)

    def get_formatted_json(self,
                           not_formatted_court_serializer: serializers.CourtNameSerializer) -> serializers.CourtNameSerializer:
        court_name = not_formatted_court_serializer.validated_data["value"]

        if court_name not in self.cache:
            db_court_search_result = self._get_formatted_from_db(not_formatted_court_serializer, court_name)
            if db_court_search_result is None:
                self._save_formatted_to_db(not_formatted_court_serializer, neuro_link.solveStr(court_name))
                return self._create_formatted_serializer(self.cache[not_formatted_court_serializer])


        formatted = serializers.CourtNameSerializer(
            data={"value": neuro_link.solveStr(non_formatted_court_name)}
        )

    def _create_formatted_serializer(self, formatted_court_name: str):
        formatted = serializers.CourtNameSerializer(
            data={"value": neuro_link.solveStr(formatted_court_name)}
        )

        return formatted

    def _save_formatted_to_db(self, non_formatted_court_name: str,
                              formatted_court_name: str):
        internal_serializer = serializers.CourtNameSerializer(data={'value': formatted_court_name})
        internal_serializer.save()
        internal_non_formatted_serializer = serializers.C(
            data={
                'value': non_formatted_court_name,
                'model': models.CourtName.objects.filter(value = formatted_court_name)
                })
        internal_non_formatted_serializer.save()
        self.cache[non_formatted_court_name] = formatted_court_name

    def _get_formatted_from_db(self, not_formatted_court_serializer: serializers.CourtNameSerializer, value: str):
        filter_result = not_formatted_court_serializer.objects.filter(value = )

        if filter_result: return filter_result[0]

        return None
