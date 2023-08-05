from collections import defaultdict
import re
import os

from ..archives.term_manager import TermManager, NoFQEntry
from ..contexts import Context, NullContext
from .quelled_cf import QuelledCF
from .clookup import CLookup, SCLookup

from synonym_dict import TermExists, FlowablesDict
# from synonym_dict.example_compartments.compartment_manager import InconsistentLineage  # this is not needed


'''
Switchable biogenic CO2:

* Biogenic CO2 is CO2, so the flowable used to store CFs is 124-38-9 always
* Because flowable is looked up within the quantity implementation, we can assign a synonym to the flow itself, and 
  watch for it
* Then the switch determines whether or not to quell the CF returned to the user, without changing the database
'''
biogenic = re.compile('(biotic|biogenic|non-fossil|in air)', flags=re.IGNORECASE)


DEFAULT_CONTEXTS = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'contexts.json'))
NUM_DEFAULT_CONTEXTS = 36  # added river, long-term

DEFAULT_FLOWABLES = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'flowables.json'))

class QuantityMasqueradeError(Exception):
    pass


class LciaEngine(TermManager):
    """
    This adds several abilities:
     * track flowables by origin
       - identify flowables thhat are not recognized
       - return flowables by origin (all, or only new)
     * lookup CFs based on context hierarchy
       - dist = 0: only exact matchh
       - dist = 1: match or subcompartments
       - dist = 2: match, subcompartments, or parent
       - dist = 3: .. or any parent up to NullContext
     * quell biogenic CO2 in quantity relation lookups
    """
    _quell_biogenic = None

    def _configure_flowables(self, flowables):
        """
        Setup local flowables database with flows that require special handling. Also loads the flowables file.

        When overriding this function, place the super() call between pre-load and post-load activities.
        :return:
        """
        if flowables is None:
            flowables = DEFAULT_FLOWABLES

        # FlowablesDict-- mainly to upsample CAS numbers for matching
        self._fm = FlowablesDict()

        self._fm.new_entry('carbon dioxide', '124-38-9')
        self._fm.new_entry('Water', '7732-18-5')
        # we store the child object and use it to signify biogenic CO2 to optionally quell
        # this strategy depends on the ability to set a query flow's name-- i.e. FlowInterface
        self._bio_co2 = self._fm.new_entry('carbon dioxide (biotic)', '124-38-9', create_child=True)

        # now load + merge from file
        self._fm.load(flowables)

        # now add all known "biotic" synonyms for CO2 to the biotic child
        for k in self._fm.synonyms('124-38-9'):
            if bool(biogenic.search(k)):
                self._bio_co2.add_term(k)
        self._fq_map = {fb: set() for fb in self._fm.objects}

    def __init__(self, contexts=None, flowables=None, quantities=None,
                 quell_biogenic_co2=False,
                 strict_clookup=True,
                 **kwargs):
        """

        :param quantities:
        :param quell_biogenic_co2:
        :param contexts:
        :param flowables:
        :param strict_clookup: [True] whether to prohibit multiple CFs for each quantity / flowable / context tuple
        :param kwargs: from TermManager: quiet, merge_strategy
        """
        if contexts is None:
            contexts = DEFAULT_CONTEXTS
        super(LciaEngine, self).__init__(contexts=contexts, flowables=None, quantities=quantities, **kwargs)

        # override flowables manager
        self._configure_flowables(flowables)

        # the CF lookup: allow hierarchical traversal over compartments [or, um, use a graph db..]
        self._cl_typ = {True: SCLookup,
                        False: CLookup}[strict_clookup]  #
        # another reverse mapping
        self._origins = set()
        self._fb_by_origin = defaultdict(set)  # maps origin to flowables having that origin
        self._fb_by_origin[None] = set(str(k) for k in self._fm.objects)

        # difficult problem, this
        self.quell_biogenic_co2 = quell_biogenic_co2

        self._factors_for_later = defaultdict(bool)

    @property
    def quell_biogenic_co2(self):
        return self._quell_biogenic

    @quell_biogenic_co2.setter
    def quell_biogenic_co2(self, value):
        self._quell_biogenic = bool(value)

    def save_for_later(self, quantity):
        qc = self.get_canonical(quantity)
        if qc is quantity:
            raise QuantityMasqueradeError(quantity)
        self._factors_for_later[qc] = quantity

    def __getitem__(self, item):
        """
        LciaEngine.__getitem__ retrieves a canonical context by more intensively searching for matches from a given
        context.  Adds foreign context's full name as synonym if one is affirmatively found.  If one is not found,
        returns the NullContext.

        None is returned as None, to represent 'unspecified' (i.e. accept all) as opposed to 'no context' which isa
        context (accept only matching). (as tested)

        :param item:
        :return: a matching context or NullContext.
        """
        if item is None:
            return None
        try:
            return self._cm.__getitem__(item)
        except KeyError:
            if isinstance(item, Context):
                return self._cm.find_matching_context(item)
            return NullContext

    def apply_hints(self, names, hints):
        """
        Hints should be
        :param names: iterable of catalog names to which context hints will apply
        :param hints: an iterable of term, canonical pairs, where term is the context as known in the origin, and
        canonical is the corresponding canonical context.
        :return:
        """
        orgs = list(names)
        for hint_type, term, canonical in hints:
            if term in self.synonyms(canonical):
                continue
            if hint_type == 'context':
                for org in orgs:
                    print('Applying context hint %s:%s => %s' % (org, term, canonical))
                    self._cm.add_context_hint(org, term, canonical)
            elif hint_type == 'quantity':
                print('Applying quantity hint %s -> %s' % (term, canonical))
                try:
                    self._qm.add_synonym(canonical, term)
                except TermExists:
                    assert self._qm[canonical] is self._qm[term]
            elif hint_type == 'flowable':
                print('Applying flowable hint %s -> %s' % (term, canonical))
                try:
                    self._fm.add_synonym(canonical, term)
                except TermExists:
                    assert self._fm[canonical] == self._fm[term]
            else:
                raise ValueError('Unknown hint type %s' % hint_type)

    def add_synonym(self, existing_term, synonym):
        """

        :param existing_term: flowable or quantity (cx is TBD)
        :param synonym: string term to add
        :return:
        """
        synonym = str(synonym).strip()
        try:
            ent = self._fm[existing_term]
            self._fm.add_synonym(ent, synonym)
        except KeyError:
            try:
                ent = self._qm[existing_term]
                self._qm.add_synonym(ent, synonym)
            except KeyError:
                raise KeyError('No entry found for %s' % existing_term)

    @staticmethod
    def _flow_terms(flow):
        """
        This function was created because we don't want TermManagers getting confused about things like misassigned
        CAS numbers, because they don't have the capacity to store multiple CFs.  So we will save the full synonym
        list for the LciaEngine.
        :param flow:
        :return:
        """
        return flow.synonyms

    def _add_flow_terms(self, flow, merge_strategy=None):
        """
        Subclass handles two problems: tracking flowables by origin and biogenic CO2.

        Should probably test this shit

        Under our scheme, it is a requirement that the flowables list used to initialize the LciaEngine is curated.

        biogenic: if ANY of the flow's terms match the biogenic regex AND the flow is CO2, set its name
        :param flow:
        :return:
        """
        fb = super(LciaEngine, self)._add_flow_terms(flow, merge_strategy=merge_strategy)
        self._fb_by_origin[flow.origin].add(str(fb))
        if '124-38-9' in fb:
            try:
                bio = next(t for t in flow.synonyms if bool(biogenic.search(t)))
            except StopIteration:
                # no biogenic terms
                return fb
            self._bio_co2.add_term(bio)  # ensure that bio term is a biogenic synonym
            flow.name = bio  # ensure that flow's name shows up with that term
            self._fb_by_origin[flow.origin].add(bio)
        return fb

    def add_quantity(self, quantity):
        """
        Here we are not picky about having duplicate quantities
        :param quantity:
        :return:
        """
        if quantity.entity_type != 'quantity':
            raise TypeError('Must be quantity type')
        if quantity.link not in self._qm:
            self._qm.add_quantity(quantity)
            assert quantity.link in self._qm
        return self._canonical_q(quantity)

    '''
    def get_canonical(self, quantity):
        """
        Override TermManager default to automatically add unknown quantities
        :param quantity:
        :return:
        """
        try:
            return self._canonical_q(quantity)
        except KeyError:
            if hasattr(quantity, 'entity_type') and quantity.entity_type == 'quantity' and not quantity.is_entity:
                print('Missing canonical quantity-- adding to LciaDb')
                self._catalog.register_quantity_ref(quantity)
                q_can = self._tm.get_canonical(quantity)
    '''

    def merge_quantities(self, first, second):
        """
        Absorb second into child of first.  Currently does not support remapping entries, so import_cfs(second)
        needs to be run again. Old factors will be left in so _fq_map still works.
        :param first:
        :param second:
        :return:
        """
        dom = self.get_canonical(first)
        add = self.get_canonical(second)
        self._qm.merge(dom, add)
        self.import_cfs(second)

    def _add_compartments(self, comps):
        """
        For LciaEngines, we use the default behavior of ContextManager which is to first try 'attach', then fallback
        to 'rename'
        :param comps:
        :return:
        """
        return self._cm.add_compartments(comps)

    '''  # This doesn't do anything useful
    def add_subcontext(self, context, prefix, sub, origin=None):
        """

        :param context: a canonical context
        :param prefix:
        :param sub: a new subcompartment
        :param origin: [None]
        :return:
        """
        if context is NullContext or context is None or context == ():
            return context
        cx_sub = tuple(context.as_list() + ['%s-%s' % (prefix, sub)])

        try:
            cx = self._cm[cx_sub]
        except (KeyError, InconsistentLineage):
            cx = self.add_context(cx_sub, origin=origin)
        return cx
    '''

    def import_cfs(self, quantity):
        """
        Given a quantity, import its CFs into the local database.  Unfortunately this is still going to be slow because
        every part of the CF still needs to be canonicalized. The only thing that's saved is creating a new
        Characterization instance.
        :param quantity: this is a TRUE quantity whose query points to the authentic origin.
        :return:
        """
        try:
            qq = self._canonical_q(quantity)
        except KeyError:
            qq = self.add_quantity(quantity)

        count = 0
        for cf in quantity.factors():
            count += 1
            # print(cf)
            try:
                fb = self._fm[cf.flowable]
            except KeyError:
                fb = self._create_flowable(*quantity.query_synonyms(cf.flowable))

            self.add_quantity(cf.ref_quantity)  # this may lead to the creation of non-converting quantities if units mismatch

            cx = self[cf.context]

            self._qassign(qq, fb, cf, context=cx)
        self._factors_for_later[quantity] = True
        print('Imported %d factors for %s' % (count, quantity))

    def _check_factors(self, qq):
        if hasattr(self._factors_for_later[qq], 'factors'):
            self.import_cfs(self._factors_for_later.pop(qq))

    def _find_exact_cf(self, qq, fb, cx, origin, flowable):
        try:
            ql = self._qlookup(qq, fb)
        except NoFQEntry:
            return None
        # cfs = ql._context_origin(cx, origin=origin)
        # if fb is self._fm['water']:  # this is not how to handle this
        #     cx = self.add_subcontext(cx, 'flow', flowable)
        cfs = ql.find(cx, dist=0, origin=origin)  # sliiiiightly slower but much better readability
        if len(cfs) > 0:
            if len(cfs) > 1:  # can only happen if qq's origin is None ??
                try:
                    return next(cf for cf in cfs if cf.origin is None)
                except StopIteration:
                    # this should never happen
                    return next(cf for cf in cfs if cf.origin == qq.origin)
            return list(cfs)[0]
        return None

    @staticmethod
    def _store_cf(cl, context, new_cf):
        """
        Assigns the cf to the mapping; does subclass-specific collision checking
        :param cl:
        :param new_cf:
        :return:
        """
        try:
            cl.add(new_cf, key=context)
        except TypeError:
            print(type(cl))
            raise

    def _qassign(self, qq, fb, new_cf, context=None):
        """

        :param qq:
        :param fb:
        :param new_cf:
        :param context:
        :return:
        """
        ''' # this is done in _find_exact_cf already
        # don't characterize "Water" per se-- give it a subcontext
        if context is not NullContext and fb is self._fm['Water']:
            context = self.add_subcontext(context, 'flow', new_cf.flowable)
        '''

        super(LciaEngine, self)._qassign(qq, fb, new_cf, context)
        self._origins.add(new_cf.origin)

    def merge_flowables(self, dominant, *syns):
        for syn in syns:
            self._fm.merge(dominant, syn)

    def save_flowables(self, filename=None):
        self._fm.save(filename)

    def save_contetxts(self, filename=None):
        self._cm.save(filename)

    def flowables(self, search=None, origin=None, new=False, **kwargs):
        """
        Adds ability to filter by origin-- note this is exclusive to the ability to filter by quantity
        :param search:
        :param origin:
        :param new: [False] if True, only return flowables that were not known originally
        :return: generates flowable strings
        """
        if origin is None:
            _iter = super(LciaEngine, self).flowables(search=search, **kwargs)
        else:
            if search is None:
                _iter = self._fb_by_origin[origin]
            else:
                _iter = (str(x) for x in self._fm.objects_with_string(search) if x in self._fb_by_origin[origin])

        for k in _iter:
            if new:
                if k in self._fb_by_origin[None]:
                    continue
            yield k

    @staticmethod
    def is_biogenic(term):
        return bool(biogenic.search(term))

    def _quell_co2(self, flowable, context):
        """
        We assume that all biogenic CO2 flows will be detected via add_flow, and will have their names set to something
        known to our _bio_co2 Flowable. So: If we are quelling, and if the flowable (string) is synonym to _bio_co2,
        we ask if it is a resource from air, or if it is any emission.
        :param flowable: orig, not looked-up in _fm
        :param context: from CF
        :return: bool
        """
        if self._quell_biogenic is False:
            return False
        if flowable in self._bio_co2:
            if context.is_subcompartment(self._cm['from air']):
                return True
            if context.is_subcompartment(self._cm['Emissions']):
                return True
        return False

    def _factors_for_flowable(self, fb, qq, cx, **kwargs):
        """
        detach lookup for cleanness. canonical everything
        :param fb:
        :param qq:
        :param cx:
        :param kwargs: used in subclasses
        :return:
        """
        self._check_factors(qq)
        try:
            cl = self._qlookup(qq, fb)
        except NoFQEntry:
            return
        if cx is None:
            for v in cl.cfs():
                yield v
        else:
            for v in cl.find(cx, **kwargs):
                yield v

    def factors_for_flowable(self, flowable, quantity=None, context=None, **kwargs):
        """
        Here we deal with water contexts specified as flowables by creating children- this is generalizeable (vs for CO2)
        :param flowable:
        :param quantity:
        :param context:
        :param kwargs:
        :return:
        """
        try:
            fb = self._fm[flowable]
        except KeyError:
            return
        '''  # this does not do anything helpful
        if fb == self._fm['Water']:
            try:
                context = self._cm['flow-%s' % flowable]
            except KeyError:
                pass
        '''
        for k in super(LciaEngine, self).factors_for_flowable(flowable, quantity=quantity, context=context, **kwargs):
            if self._quell_co2(flowable, context):
                yield QuelledCF.from_cf(k, flowable=self._bio_co2)
            else:
                yield k

    def factors_for_quantity(self, quantity, flowable=None, context=None, **kwargs):
        self._check_factors(self._canonical_q(quantity))
        return super(LciaEngine, self).factors_for_quantity(quantity, flowable=flowable, context=context, **kwargs)


    def _serialize_qdict(self, origin, quantity, values=False):
        _ql = self._qaccess(quantity)
        d = {}
        for fb, cl in _ql.items():
            _od = cl.serialize_for_origin(origin, values=values)
            if len(_od) > 0:
                d[str(fb)] = _od
        return d
