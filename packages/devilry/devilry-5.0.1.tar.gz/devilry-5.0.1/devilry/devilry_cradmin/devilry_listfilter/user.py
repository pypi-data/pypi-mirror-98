from django.utils.translation import ugettext_lazy
from cradmin_legacy.viewhelpers import listfilter


class Search(listfilter.django.single.textinput.Search):
    def __init__(self, label_is_screenreader_only=True):
        super(Search, self).__init__(
            slug='search',
            label=ugettext_lazy('Search'),
            label_is_screenreader_only=label_is_screenreader_only
        )

    def get_placeholder(self):
        return ugettext_lazy('Search listed objects ...')

    def get_modelfields(self):
        return [
            'fullname',
            'shortname',
            'username__username',
            'useremail__email',
        ]
