"""
This module provides a routine that generates a list of exchange refs from a properly formatted spreadsheet
"""
from .refs import CatalogRef, ExchangeRef
from .interfaces import check_direction


def _row_dict(sheetlike, row):
    """
    Creates a dictionary from the named row of the 'sheetlike' input.
    :param sheetlike: has row() method returns a list of strings
    :param row: int
    :return: dict k: v where k are entry.value.lower() for entry in row(0) and v are entry.value for entry in row(row)
    """
    headers = [k.value.lower() for k in sheetlike.row(0)]
    return {headers[i]: k.value for i, k in enumerate(sheetlike.row(row)) if i < len(headers)}


def _popanykey(dct, *keys, strict=False):
    """
    Returns the first of the listed keys to be found in the dict
    :param dct: a dict
    :param keys:
    :param strict: [False] if True, raise KeyError if we get to the end of the list and nothing was found
    :return:
    """
    for key in keys:
        if key in dct:
            return dct.pop(key)
    if strict:
        raise KeyError(keys)
    return None


def _exchange_params(origin, rowdict):
    """
    This is the excel file parser that specifies how to create an exchange ref heuristically from a varied list of
    potentially valid column namings.  This could be used equally well with JSON
    :param rowdict:
    :return:
    """
    rowdict.pop('process', None)
    flow_ref = _popanykey(rowdict, 'flow', 'flowref', 'flow_ref', 'external_ref', strict=True)
    flow = CatalogRef(origin, flow_ref, entity_type='flow')
    dirn = check_direction(_popanykey(rowdict, 'direction', 'flowdir', strict=True))
    try:
        value = float(_popanykey(rowdict, 'value', 'amount', strict=True))
    except ValueError:
        value = 0.0
    unit = _popanykey(rowdict, 'unit', 'units')
    term = _popanykey(rowdict, 'context', 'compartment')
    if term == '':
        term = None
    print('%s %s %g %s [%s]' % (flow, dirn, value, unit, term))
    return flow, dirn, value, unit, term


def exchanges_from_spreadsheet(sheetlike, term_dict, node=None, origin=None):
    """
    A routine to create a list of flat exchanges (all having the same parent node) from an excel table.

    Note that this only creates a sequence of exchange refs with strings as properties, plus an inoperable process_ref
    for the parent node.  These could be used to construct a foreground model but do not by themselves constitute
    a foreground model.

    Requirements for the sheet-like object:
     - name property that returns a string
     - nrows property that reports the number of rows
     - row(index) function that returns an ordered list of entries for the specified index (0-indexed).
     - row(0) returns a header list
     - row(1) is the process's reference flow
     - subsequent rows are dependent flows
     !TODO: support multiple references with is_ref or is_reference field

    "entries" in the row() return must be "cell-like":
     - value property that returns the cell's value
     - ctype property [*not currently used*] that corresponds with xlrd.sheet.Cell:
        0=empty, 1=text, 2=number, 3=date, 4=boolean, 5=error, 6=blank
        (not clear what the difference is between empty and blank)

    Columns are interpreted as follows (case-insensitive):
    Required:
    'flow', 'flowref', 'flow_ref', 'external_ref' - in that order, used to specify flow
    'direction', 'flowdir' - in that order, used to specify direction w.r.t. parent node
    'value', 'amount' - in that order
    This method returns unresolved catalog refs- in order for client code to use them, the flow refs must resolve (bc
    reference quantity must be known and is not required to be specified)

    Optional
    'unit', 'units' - unit of measure for the flow
    'context', 'compartment' - used to determine the termination of the exchange, default to None

    Ignored:
    'process' - ignored

    :param sheetlike: an Xlrd-like object with name, nrows, and row() 
    :param term_dict: a dict mapping context / category / flow external_ref to termination
    :param node: [None] if present, use as exchange parent node for all exchanges
    :param origin: ['local.spreadsheet'] Should be provided by caller if 'node' is omitted, to give identifying 
      information to the created process
    :return:
    """
    """
    First one is the reference; subsequent ones are child flows
    sheetlike: 
    term_dict: a dictionary mapping strings found in "context", "compartment", or "flow" columns (in that order) to
     terminations.
    """
    if origin is None:
        origin = 'local.spreadsheet'
    if node is None:
        proc_ref = CatalogRef(origin, sheetlike.name, entity_type='process')
    else:
        proc_ref = node
    ref_flow = _row_dict(sheetlike, 1)
    flow_ref, dirn, value, units, term = _exchange_params(origin, ref_flow)
    if term is not None:
        raise ValueError('(%s) Reference flow cannot have specified termination: %s' % (sheetlike.name, term))
    # reference flow is unterminated
    yield ExchangeRef(proc_ref, flow_ref, dirn, value=value, unit=units, is_reference=True, **ref_flow)

    for row in range(2, sheetlike.nrows):
        c_flow = _row_dict(sheetlike, row)
        try:
            flow_ref, dirn, value, units, term = _exchange_params(origin, c_flow)
        except KeyError:
            print('Skipping poorly defined row %d\n%s' % (row, c_flow))
            continue
        if term in term_dict:
            term = term_dict[term]
        elif term is None:
            if flow_ref.external_ref in term_dict:
                term = term_dict[flow_ref.external_ref]
        yield ExchangeRef(proc_ref, flow_ref, dirn, value=value, unit=units, termination=term, **c_flow)
