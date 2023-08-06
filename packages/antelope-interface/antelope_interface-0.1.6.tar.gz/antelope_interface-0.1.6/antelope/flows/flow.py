from .flow_interface import FlowInterface

from synonym_dict import SynonymSet


class Flow(FlowInterface):
    """
    A partly-abstract class that implements the flow specification but not the entity specification.
    """

    _context = ()
    _context_set_level = 0

    _filt = str.maketrans('\u00b4\u00a0\u2032', "' '", '')  # filter name strings to pull out problematic unicode

    def _catch_context(self, key, value):
        """
        Add a hook to set context in __getitem__ or wherever is appropriate, to capture and automatically set context
        according to the following precedence:
         context > compartment > category > class | classification > cutoff (default)
        :param key:
        :param value:
        :return:
        """
        try:
            level = {'none': 0,
                     'class': 1,
                     'classification': 1,
                     'classifications': 1,
                     'category': 2,
                     'categories': 2,
                     'compartment': 3,
                     'compartments': 3,
                     'context': 4}[key.lower()]
        except KeyError:
            return
        if isinstance(value, str):
            value = (value, )
        if level > self._context_set_level:
            self._context_set_level = min([level, 3])  # always allow context spec to override
            self._context = tuple(filter(None, value))

    def _add_synonym(self, term, set_name=False):
        if set_name:
            tm = term.translate(self._filt).strip()  # have to put strip after because \u00a0 turns to space
            self._flowable.add_term(tm)
            self._flowable.set_name(tm)
        self._flowable.add_term(term.strip())

    def _catch_flowable(self, key, value):
        """
        Returns True or None- allow to chain to avoid redundant _catch_context
        :param key:
        :param value:
        :return:
        """
        if key == 'name':
            self._add_synonym(value, set_name=True)
            return True
        elif key == 'casnumber':
            self._add_synonym(value)
            return True
        elif key == 'synonyms':
            if isinstance(value, str):
                self._add_synonym(value)
                return True
            else:
                for v in value:
                    self._add_synonym(v)
                return True

    __flowable = None

    @property
    def _flowable(self):
        if self.__flowable is None:
            self.__flowable = SynonymSet()
        return self.__flowable

    @property
    def name(self):
        return self._flowable.name

    @name.setter
    def name(self, name):
        """

        :param name:
        :return:
        """
        if name is None:
            raise TypeError('None is not a valid name')
        elif name in self.synonyms:
            self._flowable.set_name(name)
        else:
            raise ValueError('name %s not a recognized synonym for %s' % (name, self.name))

    @property
    def synonyms(self):
        for t in self._flowable.terms:
            yield t

    @property
    def context(self):
        """
        A flow's context is any hierarchical tuple of strings (generic, intermediate, ..., specific).
        :return:
        """
        return self._context

    @context.setter
    def context(self, value):
        self._catch_context('Context', value)

    def match(self, other):
        """
        match if any synonyms match
        :param other:
        :return:
        """
        '''
        return (self.uuid == other.uuid or
                self['Name'].lower() == other['Name'].lower() or
                (trim_cas(self['CasNumber']) == trim_cas(other['CasNumber']) and len(self['CasNumber']) > 4) or
                self.external_ref == other.external_ref)  # not sure about this last one! we should check origin too
        '''
        if isinstance(other, str):
            return other in self._flowable
        return any([t in self._flowable for t in other.synonyms])

