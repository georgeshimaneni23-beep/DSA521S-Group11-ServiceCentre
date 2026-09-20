"""Schema-correct insertion of child elements into w:tblPr and w:pPr."""
from docx.oxml.ns import qn

TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
               "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
               "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption", "tblDescription"]

PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
             "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
             "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE",
             "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
             "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
             "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
             "sectPr", "pPrChange"]


def insert_ordered(parent, child, order):
    tag = child.tag.split("}")[1]
    idx = order.index(tag)
    for existing in parent:
        name = existing.tag.split("}")[1]
        if name in order and order.index(name) > idx:
            existing.addprevious(child)
            return
    parent.append(child)


def add_tbl_pr(tblPr, child):
    insert_ordered(tblPr, child, TBLPR_ORDER)


def add_p_pr(pPr, child):
    insert_ordered(pPr, child, PPR_ORDER)
