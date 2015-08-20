from django.conf.urls import url, include
from . import constants
from .views_convert import ReferenceConvertList1, ReferenceConvertList2, ReferenceConvertList3, ReferenceConvertList4, ReferenceConvertList5, ReferenceConvertCreate, ReferenceConvertDelete, ReferenceConvertUpdate
from .views_home import HomeView
from .views_reference_key_value import ReferenceKeyValueList, ReferenceKeyValueCreate, ReferenceKeyValueDelete, ReferenceKeyValueUpdate, ReferenceKeyValueDetail
from .views_systemsource import SystemSourceList, SystemSourceCreate, SystemSourceUpdate, SystemSourceDelete, SystemSourceDetail, SystemSourceFilter, SystemSourceUpload, SystemSourceDownload
from .views_reference import ReferenceList, ReferenceCreate, ReferenceDetail, ReferenceUpdate, ReferenceDelete

reference_key_value_urls = [
    url(r"^$", ReferenceKeyValueList.as_view(), name="ref_kvp_list"),
    url(r"^create$", ReferenceKeyValueCreate.as_view(), name="ref_kvp_create"),
    url(r"^(?P<ref_key>" + constants.code + ")/update$", ReferenceKeyValueUpdate.as_view(), name="ref_kvp_update"),
    url(r"^(?P<ref_key>" + constants.code + ")/delete$", ReferenceKeyValueDelete.as_view(), name="ref_kvp_delete"),
    url(r"^(?P<ref_key>" + constants.code + ")/detail$", ReferenceKeyValueDetail.as_view(), name="ref_kvp_detail"),
]

reference_urls = [
    url(r"^$", ReferenceList.as_view(), name="ref_list"),
    url(r"^create$", ReferenceCreate.as_view(), name="ref_create"),
    url(r"^(?P<ref>" + constants.code + ")/update$", ReferenceUpdate.as_view(), name="ref_update"),
    url(r"^(?P<ref>" + constants.code + ")/delete$", ReferenceDelete.as_view(), name="ref_delete"),
    url(r"^(?P<ref>" + constants.code + ")/$", ReferenceDetail.as_view(), name="ref_detail"),
    url(r"^(?P<ref>" + constants.code + ")/content/", include(reference_key_value_urls)),
]

system_urls = [
    url(r"^$", SystemSourceList.as_view(), name="ss_list"),
    url(r"^create$", SystemSourceCreate.as_view(), name="ss_create"),
    url(r"^(?P<sys>" + constants.code + ")/update/$", SystemSourceUpdate.as_view(), name="ss_update"),
    url(r"^(?P<sys>" + constants.code + ")/delete/$", SystemSourceDelete.as_view(), name="ss_delete"),
    url(r"^(?P<sys>" + constants.code + ")/$", SystemSourceDetail.as_view(), name="ss_detail"),
    url(r"^(?P<sys>" + constants.code + ")/references/", include(reference_urls)),
    url(r"^(?P<sys>" + constants.code + ")/download/", SystemSourceDownload.as_view(), name="ss_download"),
    url(r"^filter/$", SystemSourceFilter.as_view(), name="ss_filter"),
    url(r"^upload", SystemSourceUpload.as_view(), name="ss_upload"),
]

convert_mgr_urls = [
    url(r"^$", ReferenceConvertList5.as_view(), name="ref_conv_list5"),
    url(r"^create/$", ReferenceConvertCreate.as_view(), name="ref_conv_create"),
    url(r"^(?P<key_from>" + constants.code + ")-(?P<key_to>" + constants.code + ")/delete/$", ReferenceConvertDelete.as_view(), name="ref_conv_delete"),
    url(r"^(?P<key_from>" + constants.code + ")-(?P<key_to>" + constants.code + ")/update/$", ReferenceConvertUpdate.as_view(), name="ref_conv_update"),
]

convert_urls = [
    url(r"^$", ReferenceConvertList1.as_view(), name="ref_conv_list1"),
    url(r"^from-(?P<sys_from>" + constants.code + ")/$", ReferenceConvertList2.as_view(), name="ref_conv_list2"),
    url(r"^from-(?P<sys_from>" + constants.code + ")-(?P<ref_from>" + constants.code + ")/$", ReferenceConvertList3.as_view(), name="ref_conv_list3"),
    url(r"^from-(?P<sys_from>" + constants.code + ")-(?P<ref_from>" + constants.code + ")-to-(?P<sys_to>" + constants.code + ")/$", ReferenceConvertList4.as_view(), name="ref_conv_list4"),
    url(r"^from-(?P<sys_from>" + constants.code + ")-(?P<ref_from>" + constants.code + ")-to-(?P<sys_to>" + constants.code + ")-(?P<ref_to>" + constants.code + ")/", include(convert_mgr_urls)),
]

urlpatterns = [
    url(r"^$", HomeView.as_view(), name="home"),
    url(r"^system/", include(system_urls)),
    url(r"^convert/", include(convert_urls)),
]
