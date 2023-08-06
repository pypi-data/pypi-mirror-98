
"""
The given file contains the class to refer to the asset entity
"""
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.iterators.tag_data_iterator import TagDataIterator


class Asset(Base):
    """
    The given class refers to the asset entity which is created based upon the
    asset object returned from the API
    """

    def __repr__(self):
        """
        Override the method to return the asset name with id
        """
        return f"<{Constants.ASSET_ENTITY}: {self.name}_{self.id}>"

    def get_tags(self):
        """
        The given method returns the list of tags for the given asset
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        tags_response = self.api_helper.call_api(
            Constants.GET_TAGS, Constants.API_GET, path_params=[], query_params={"asset": self.id}).json()
        return EntityFactory(Constants.TAG_ENTITY, tags_response, self.api_helper)

    def event_frames(self):
        """
        The given method returns the list of event frames for the given asset
        """
        raise NotImplementedError

    def batches(self):
        """
        The given method returns the list of batches for the given asset
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        batches_response = self.api_helper.call_api(
            Constants.GET_BATCHES, Constants.API_GET, [self.id]).json()
        return EntityFactory(
            Constants.BATCH_ENTITY,
            batches_response,
            self.api_helper)

    def data(
            self,
            start_time,
            stop_time,
            granularity=0,
            return_type=Constants.RETURN_PANDAS,
            transformations=[]):
        """
        Get the data of all tags in the asset between the given start_time and
        stop_time for the given granularity
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param granularity: Granularity of the data
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"}
            }]
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        tags = self.get_tags()
        return TagDataIterator.create_tag_data_iterator(
            tags,
            start_time,
            stop_time,
            self.api_helper,
            granularity,
            return_type,
            transformations)
