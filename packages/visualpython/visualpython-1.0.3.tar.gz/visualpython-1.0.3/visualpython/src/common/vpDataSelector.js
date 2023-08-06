define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
], function (requirejs, $, vpConst, sb, vpCommon, vpSuggestInputText, pdGen) {


    // Temporary constant data
    const VP_DS_BTN = 'vp-ds-button';
    const VP_DS = 'vp-ds';
    const VP_DS_CONTAINER = 'vp-ds-container';
    const VP_DS_CLOSE = 'vp-ds-close';
    const VP_DS_TITLE = 'vp-ds-title';
    const VP_DS_BODY = 'vp-ds-body';

    const VP_DS_PREVIEW = 'vp-ds-preview';

    const VP_DS_PANDAS_OBJECT = 'vp-ds-pandas-object';
    const VP_DS_USE_COPY = 'vp-ds-use-copy';

    const VP_DS_SUBSET_TYPE = 'vp-ds-subset-type';
    const VP_DS_TO_FRAME = 'vp-ds-to-frame';

    /** tab selector */
    const VP_DS_TAB_SELECTOR_BOX = 'vp-ds-tab-selector-box';
    const VP_DS_TAB_SELECTOR_BTN = 'vp-ds-tab-selector-btn';
    /** tab page */
    const VP_DS_TAB_PAGE = 'vp-ds-tab-page';
    const VP_DS_TAB_PAGE_BOX = 'vp-ds-tab-page-box';

    const VP_DS_ROWTYPE = 'vp-ds-rowtype';
    const VP_DS_ROWTYPE_BOX = 'vp-ds-rowtype-box';

    /** indexing timestamp */
    const VP_DS_INDEXING_TIMESTAMP = 'vp-ds-indexing-timestamp';

    /** select */
    const VP_DS_SELECT_CONTAINER = 'vp-ds-select-container';
    const VP_DS_SELECT_LEFT = 'vp-ds-select-left';
    const VP_DS_SELECT_BTN_BOX = 'vp-ds-select-btn-box';
    const VP_DS_SELECT_RIGHT = 'vp-ds-select-right';

    const VP_DS_SELECT_BOX = 'vp-ds-select-box';
    const VP_DS_SELECT_ITEM = 'vp-ds-select-item';
    
    /** select left */
    const VP_DS_SELECT_SEARCH = 'vp-ds-select-search';
    const VP_DS_DROPPABLE = 'vp-ds-droppable';
    const VP_DS_DRAGGABLE = 'vp-ds-draggable';

    /** select btns */
    const VP_DS_SELECT_ADD_BTN = 'vp-ds-select-add-btn';
    const VP_DS_SELECT_DEL_BTN = 'vp-ds-select-del-btn';

    /** slicing box */
    const VP_DS_SLICING_BOX = 'vp-ds-slicing-box';

    /** row slice */
    const VP_DS_ROW_SLICE_START = 'vp-ds-row-slice-start';
    const VP_DS_ROW_SLICE_END = 'vp-ds-row-slice-end';

    /** row condition */
    const VP_DS_CONDITION_TBL = 'vp-ds-cond-tbl';

    
    /** column selection/slicing */
    const VP_DS_COLTYPE = 'vp-ds-coltype';
    const VP_DS_COLTYPE_BOX = 'vp-ds-coltype-box';

    /** column slice */
    const VP_DS_COL_SLICE_START = 'vp-ds-col-slice-start';
    const VP_DS_COL_SLICE_END = 'vp-ds-col-slice-end';

    /** data view */
    const VP_DS_DATA_VIEW_ALL_DIV = 'vp-ds-data-view-all-div';
    const VP_DS_DATA_VIEW_ALL = 'vp-ds-data-view-all';
    const VP_DS_DATA_VIEW_BOX = 'vp-ds-data-view-box';

    /** buttons */
    const VP_DS_BUTTON_BOX = 'vp-ds-btn-box';
    const VP_DS_BUTTON_APPLY = 'vp-ds-btn-apply';
    const VP_DS_BUTTON_CANCEL = 'vp-ds-btn-cancel';
    /** preview code */
    const VP_DS_BUTTON_PREVIEW = 'vp-ds-btn-preview';

    const STYLE_REQUIRED_LABEL = 'vp-orange-text';

    /**
     * @class DataSelector
     * @param {object} pageThis
     * @param {string} targetId
     * @constructor
     */
    var DataSelector = function(pageThis, targetId) {
        this.pageThis = pageThis;
        this.targetId = targetId;
        this.uuid = vpCommon.getUUID();

        // specify pandas object types
        this.pdObjTypes = ['DataFrame', 'Series'];

        this.state = {
            viewAll: false,

            // all variables list on opening popup
            dataList: [],
            pandasObject: '',
            dataType: '',
            isTimestamp: false,     // is df.index timestampindex? true / false

            useCopy: false,
            toFrame: true,
            subsetType: 'subset',   // subset / loc / iloc

            tabPage: 'subset',      // subset / data

            rowType: 'indexing',    // indexing / slicing / condition
            rowList: [],
            rowPointer: { start: -1, end: -1 },

            colType: 'indexing',      // indexing / slicing
            columnList: [],
            colPointer: { start: -1, end: -1 }
        }
        
        this.bindEvent();
        this.init();
        this.loadVariables();
    }

    /**
     * Initialize DataSelector's variables
     * & set button next to input tag
     */
    DataSelector.prototype.init = function() {
        // load css
        this.pageThis.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "common/dataSelector.css");

        // Init variables

        // set button next to input tag
        var buttonTag = new sb.StringBuilder();
        buttonTag.appendFormat('<button type="button" class="{0} {1}">{2}</button>'
                                , VP_DS_BTN, this.uuid, '...');
        $(this.pageThis.wrapSelector('#' + this.targetId)).parent().append(buttonTag.toString());

        // add popup div
        var popupTag = new sb.StringBuilder();
        popupTag.appendFormat('<div class="{0} {1}">', VP_DS, this.uuid);
        popupTag.appendFormat('<div class="{0}">', VP_DS_CONTAINER);
        
        // title
        popupTag.appendFormat('<div class="{0}">{1}</div>'
                            , VP_DS_TITLE
                            , 'Data Selector');

        // close button
        popupTag.appendFormatLine('<div class="{0}"><i class="{1}"></i></div>'
                                    , VP_DS_CLOSE, 'fa fa-close');

        // body start
        popupTag.appendFormatLine('<div class="{0}">', VP_DS_BODY);

        // table1 start
        popupTag.appendLine('<table>');
        popupTag.appendLine('<thead><colgroup><col width="150px"><col width="*"></colgroup></thead>');
        popupTag.appendLine('<tbody>');

        // preview code board
        popupTag.appendFormatLine('<tr><td colspan="2"><pre class="{0}"># PREVIEW CODE</pre></td></tr>', VP_DS_PREVIEW);
        
        // pandasObject
        popupTag.appendLine('<tr>');
        popupTag.appendFormatLine('<td><label class="{0}">{1}</label></td>'
                                , '', 'Variable');

        // pandasObject - suggestInputText
        var vpDfSuggest = new vpSuggestInputText.vpSuggestInputText();
        vpDfSuggest.addClass(VP_DS_PANDAS_OBJECT);
        vpDfSuggest.addClass('vp-input');
        vpDfSuggest.setPlaceholder('Select Object');
        vpDfSuggest.setSuggestList(function() { return [] });
        vpDfSuggest.setNormalFilter(false);
        vpDfSuggest.setValue($(this.pageThis.wrapSelector('#' + this.targetId)).val());

        popupTag.appendFormatLine('<td>{0}', vpDfSuggest.toTagString());
        
        // use copy
        popupTag.appendFormatLine('<label><input type="checkbox" class="{0}"/><span>{1}</span></label>', VP_DS_USE_COPY, 'Use Copy');
        popupTag.appendLine('</td></tr>');

        // subset type
        popupTag.appendLine('<tr>');
        popupTag.appendFormatLine('<td><label class="{0}">{1}</label></td>'
                                , '', 'Subset Type');
        popupTag.appendLine('<td>');
        popupTag.appendLine(this.renderSubsetType(this.state.dataType));
        
        // to frame
        popupTag.appendFormatLine('<label style="display:none;"><input type="checkbox" class="{0}" checked/><span>{1}</span></label>', VP_DS_TO_FRAME, 'To Frame');

        popupTag.appendLine('</td></tr>');

        // table1 end
        popupTag.appendLine('</tbody></table>');

        // divider
        popupTag.appendLine('<hr style="margin: 3px;"/>');

        // tab selector
        popupTag.appendFormatLine('<div class="{0}">', VP_DS_TAB_SELECTOR_BOX);
        popupTag.appendFormatLine('<div class="{0} selected" data-page="{1}">{2}</div>', VP_DS_TAB_SELECTOR_BTN, 'subset', 'Subset');
        popupTag.appendFormatLine('<div class="{0}" data-page="{1}">{2}</div>', VP_DS_TAB_SELECTOR_BTN, 'data', 'Data');
        popupTag.appendLine('</div>');

        // tab page 1 start
        popupTag.appendFormatLine('<div class="{0} {1}">', VP_DS_TAB_PAGE, 'subset');

        // row box start
        popupTag.appendFormatLine('<div class="{0} {1}">', VP_DS_TAB_PAGE_BOX, 'subset-row');
        // row type
        popupTag.appendFormatLine('<div><label class="{0}">{1}</label></td>'
                                , '', 'Row Subset');
        popupTag.appendLine(this.renderRowSubsetType(this.state.subsetType)); // VP_DS_ROWTYPE
        popupTag.appendLine('</div>');

        // row indexing
        popupTag.appendFormatLine('<div class="{0} {1}">', VP_DS_ROWTYPE_BOX, 'indexing');

        // row indexing list
        popupTag.appendLine(this.renderRowIndexing(this.state.rowList));

        popupTag.appendLine('</div>');  // VP_DS_ROWTYPE_BOX
        
        // row slicing
        popupTag.appendFormatLine('<div class="{0} {1}" style="display:none;">', VP_DS_ROWTYPE_BOX, 'slicing');

        // popupTag.appendFormatLine('<label class="{0}">{1}</label>'
        //                         , '', 'Slice');
        // popupTag.appendFormatLine('<input type="text" class="{0} {1}" placeholder="{2}"/> : ', VP_DS_ROW_SLICE_START, 'vp-input s', 'start');
        // popupTag.appendFormatLine('<input type="text" class="{0} {1}" placeholder="{2}"/>', VP_DS_ROW_SLICE_END, 'vp-input s', 'end');
        popupTag.appendLine(this.renderRowSlicingBox(this.state.rowList));
        popupTag.appendLine('</div>'); // VP_DS_ROWTYPE_BOX

        // condition box start
        popupTag.appendFormatLine('<div class="{0} {1} {2}" style="display:none;">', VP_DS_ROWTYPE_BOX, 'condition', 'no-selection');
        // row condition
        popupTag.appendFormatLine('<label class="{0}">{1}</label>'
                                , '', 'Conditional Subset');
        popupTag.appendFormatLine('{0}', this.renderColumnConditionList(this.state.columnList));
        // condition box end
        popupTag.appendLine('</div>'); // VP_DS_ROWTYPE_BOX

        // row box end
        popupTag.appendLine('</div>');

        // column box start
        popupTag.appendFormatLine('<div class="{0} {1}">', VP_DS_TAB_PAGE_BOX, 'subset-column');

        // column type
        popupTag.appendFormatLine('<div><label class="{0}">{1}</label>'
                                , '', 'Column Subset');
        popupTag.appendLine(this.renderColumnSubsetType(this.state.subsetType)); // VP_DS_COLTYPE
        popupTag.appendLine('</div>');

        // column indexing
        popupTag.appendFormatLine('<div class="{0} {1}">', VP_DS_COLTYPE_BOX, 'indexing');

        // column indexing list
        popupTag.appendLine(this.renderColumnIndexing(this.state.columnList));

        popupTag.appendLine('</div>');  // VP_DS_COLTYPE_BOX
        
        // column slicing
        popupTag.appendFormatLine('<div class="{0} {1}" style="display:none;">', VP_DS_COLTYPE_BOX, 'slicing');
        popupTag.appendLine(this.renderColumnSlicingBox(this.state.columnList));
        popupTag.appendLine('</div>'); // VP_DS_COLTYPE_BOX

        // column box end
        popupTag.appendLine('</div>');

        // tab page 1 end
        popupTag.appendLine('</div>');

        // tab page 2 start
        popupTag.appendFormatLine('<div class="{0} {1}" style="display:none;">', VP_DS_TAB_PAGE, 'data');
        // data view type
        popupTag.appendFormatLine('<div class="{0}"><label><input type="checkbox" class="{1}"/><span>{2}</span></label></div>'
                                , VP_DS_DATA_VIEW_ALL_DIV, VP_DS_DATA_VIEW_ALL, "view all");
        // data view
        popupTag.appendLine(this.renderDataPage(''));
        // tab page 2 end
        popupTag.appendLine('</div>');

        // apply button
        popupTag.appendFormatLine('<div class="{0}">', VP_DS_BUTTON_BOX);
        // popupTag.appendFormatLine('<button type="button" class="{0}">{1}</button>'
        //                         , VP_DS_BUTTON_PREVIEW, 'Preview');
        popupTag.appendFormatLine('<button type="button" class="{0}">{1}</button>'
                                , VP_DS_BUTTON_APPLY, 'Apply');
        popupTag.appendFormatLine('<button type="button" class="{0}">{1}</button>'
                                , VP_DS_BUTTON_CANCEL, 'Cancel');
        popupTag.appendLine('</div>');

        // body end
        popupTag.appendLine('</div>');

        popupTag.append('</div>');
        popupTag.append('</div>');
        // $(vpCommon.formatString("#{0}", vpConst.VP_CONTAINER_ID)).append(popupTag.toString());
        $('#vp-wrapper').append(popupTag.toString());
        $(vpCommon.formatString(".{0}.{1}", VP_DS, this.uuid)).hide();
        
    }

    /**
     * Wrap Selector for data selector popup with its uuid
     * @param {string} query 
     */
    DataSelector.prototype.wrapSelector = function(query) {
        return vpCommon.formatString('.{0}.{1} {2}', VP_DS, this.uuid, query);
    }

    ///////////////////////// render //////////////////////////////////////////////////////

    DataSelector.prototype.renderSubsetType = function(dataType) {
        var subsetType = this.state.subsetType;
        if (dataType == 'Series') {
            subsetType = 'subset';
        }

        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<select class="{0} {1}">', VP_DS_SUBSET_TYPE, 'vp-select');
        tag.appendFormatLine('<option value="{0}" {1}>{2}</option>', 'subset', subsetType == 'subset'?'selected':'', 'subset');
        if (dataType == 'DataFrame') {
            tag.appendFormatLine('<option value="{0}" {1}>{2}</option>', 'loc', subsetType == 'loc'?'selected':'', 'loc');
            tag.appendFormatLine('<option value="{0}" {1}>{2}</option>', 'iloc', subsetType == 'iloc'?'selected':'', 'iloc');
        }
        tag.appendLine('</select>');

        return tag.toString();
    }

    DataSelector.prototype.renderRowSubsetType = function(subsetType, timestamp=false) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<select class="{0} {1}">', VP_DS_ROWTYPE, 'vp-select m');
        if (subsetType == 'loc' || subsetType == 'iloc' || timestamp == true) {
            tag.appendFormatLine('<option value="{0}">{1}</option>', 'indexing', 'indexing');
        }
        tag.appendFormatLine('<option value="{0}">{1}</option>', 'slicing', 'slicing');
        if ((subsetType == 'subset' || subsetType == 'loc') && this.state.dataType == 'DataFrame') {
            tag.appendFormatLine('<option value="{0}">{1}</option>', 'condition', 'condition');
        }
        tag.appendLine('</select>');
        return tag.toString();
    }

    DataSelector.prototype.renderColumnSubsetType = function(subsetType) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<select class="{0} {1}">', VP_DS_COLTYPE, 'vp-select m');
        tag.appendFormatLine('<option value="{0}">{1}</option>', 'indexing', 'indexing');
        if (subsetType == 'loc' || subsetType == 'iloc') {
            tag.appendFormatLine('<option value="{0}">{1}</option>', 'slicing', 'slicing');
        }
        tag.appendLine('</select>');
        return tag.toString();
    }

    /**
     * Render row selection list
     * - search box
     * - row list box (left)
     * - buttons (add/del to right box)
     * - apply box (right)
     * @param {Array} rowList 
     */
    DataSelector.prototype.renderRowIndexing = function(rowList) {
        var that = this;

        var tag = new sb.StringBuilder();
        if (this.state.subsetType == 'subset' && this.state.isTimestamp) {
            // timestamp input tag
            tag.appendFormatLine('<input type="text" class="{0} {1}" placeholder="{2}" />'
                                , VP_DS_INDEXING_TIMESTAMP, 'vp-input', 'Timestamp Index');
        } else {
            tag.appendFormatLine('<div class="{0} {1}">', VP_DS_SELECT_CONTAINER, 'select-row');
            // row select - left
            tag.appendFormatLine('<div class="{0}">', VP_DS_SELECT_LEFT);
            // tag.appendFormatLine('<input type="text" class="{0}" placeholder="{1}"/>'
            //                         , VP_DS_SELECT_SEARCH, 'Search Row');
            var vpSearchSuggest = new vpSuggestInputText.vpSuggestInputText();
            vpSearchSuggest.addClass(VP_DS_SELECT_SEARCH);
            vpSearchSuggest.setPlaceholder('Search Row');
            vpSearchSuggest.setSuggestList(function() { return that.state.rowList; });
            vpSearchSuggest.setSelectEvent(function(value) {
                $(this.wrapSelector()).val(value);
                $(this.wrapSelector()).trigger('change');
            });
            vpSearchSuggest.setNormalFilter(true);
            tag.appendLine(vpSearchSuggest.toTagString());
    
            tag.appendLine(this.renderRowSelectionBox(rowList));
            tag.appendLine('</div>');  // VP_DS_SELECT_LEFT
            // row select - buttons
            tag.appendFormatLine('<div class="{0}">', VP_DS_SELECT_BTN_BOX);
            tag.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>', VP_DS_SELECT_ADD_BTN, 'select-row', '>');
            tag.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>', VP_DS_SELECT_DEL_BTN, 'select-row', '<');
            tag.appendLine('</div>');  // VP_DS_SELECT_BTNS
            // row select - right
            tag.appendFormatLine('<div class="{0}">', VP_DS_SELECT_RIGHT);
            tag.appendFormatLine('<div class="{0} {1} {2} {3}">', VP_DS_SELECT_BOX, 'right', VP_DS_DROPPABLE, 'no-selection');
            // TODO: droppable
            tag.appendLine('</div>');  // VP_DS_SELECT_BOX
            tag.appendLine('</div>');  // VP_DS_SELECT_RIGHT
            tag.appendLine('</div>');  // VP_DS_SELECT_CONTAINER
        }
        return tag.toString();
    }

    /**
     * Render row list box
     * @param {Array} rowList 
     */
    DataSelector.prototype.renderRowSelectionBox = function(rowList) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0} {1} {2} {3}">', VP_DS_SELECT_BOX, 'left', VP_DS_DROPPABLE, 'no-selection');

        // get row data and make draggable items
        rowList.forEach((row, idx) => {
            tag.appendFormatLine('<div class="{0} {1} {2}" data-idx="{3}" data-rowname="{4}" data-code="{5}" title="{6}"><span>{7}</span></div>'
                                , VP_DS_SELECT_ITEM, 'select-row', VP_DS_DRAGGABLE, row.location, row.value, row.code, row.label, row.label);
        });
        tag.appendLine('</div>');  // VP_DS_SELECT_BOX
        return tag.toString();
    }

    /**
     * Render row slicing box
     * - slicing start/end with suggestInput
     * @param {Array} rowList 
     */
    DataSelector.prototype.renderRowSlicingBox = function(rowList) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0}">', VP_DS_SLICING_BOX);
        var vpRowStart = new vpSuggestInputText.vpSuggestInputText();
        vpRowStart.addClass(VP_DS_ROW_SLICE_START);
        vpRowStart.addClass('vp-input m');
        vpRowStart.setPlaceholder('start');
        vpRowStart.setSuggestList(function() { return rowList });
        vpRowStart.setSelectEvent(function(value, item) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).attr('data-code', item.code);
            $(this.wrapSelector()).trigger('change');
        });
        vpRowStart.setNormalFilter(false);

        var vpRowEnd = new vpSuggestInputText.vpSuggestInputText();
        vpRowEnd.addClass(VP_DS_ROW_SLICE_END);
        vpRowEnd.addClass('vp-input m');
        vpRowEnd.setPlaceholder('end');
        vpRowEnd.setSuggestList(function() { return rowList });
        vpRowEnd.setSelectEvent(function(value, item) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).attr('data-code', item.code);
            $(this.wrapSelector()).trigger('change');
        });
        vpRowEnd.setNormalFilter(false);

        tag.appendLine(vpRowStart.toTagString());
        tag.appendLine(vpRowEnd.toTagString());
        tag.appendLine('</div>');
        return tag.toString();
    }

    /**
     * Render column selection list
     * - search box
     * - column list box (left)
     * - buttons (add/del to right box)
     * - apply box (right)
     * @param {Array} colList 
     */
    DataSelector.prototype.renderColumnIndexing = function(colList) {
        var that = this;

        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0} {1}">', VP_DS_SELECT_CONTAINER, 'select-col');
        // col select - left
        tag.appendFormatLine('<div class="{0}">', VP_DS_SELECT_LEFT);
        // tag.appendFormatLine('<input type="text" class="{0}" placeholder="{1}"/>'
        //                         , VP_DS_SELECT_SEARCH, 'Search Column');
        var vpSearchSuggest = new vpSuggestInputText.vpSuggestInputText();
        vpSearchSuggest.addClass(VP_DS_SELECT_SEARCH);
        vpSearchSuggest.setPlaceholder('Search Column');
        vpSearchSuggest.setSuggestList(function() { return that.state.columnList; });
        vpSearchSuggest.setSelectEvent(function(value) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).trigger('change');
        });
        vpSearchSuggest.setNormalFilter(true);
        tag.appendLine(vpSearchSuggest.toTagString());
        
        tag.appendLine(this.renderColumnSelectionBox(colList));
        tag.appendLine('</div>');  // VP_DS_SELECT_LEFT
        // col select - buttons
        tag.appendFormatLine('<div class="{0}">', VP_DS_SELECT_BTN_BOX);
        tag.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>', VP_DS_SELECT_ADD_BTN, 'select-col', '>');
        tag.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>', VP_DS_SELECT_DEL_BTN, 'select-col', '<');
        tag.appendLine('</div>');  // VP_DS_SELECT_BTNS
        // col select - right
        tag.appendFormatLine('<div class="{0}">', VP_DS_SELECT_RIGHT);
        tag.appendFormatLine('<div class="{0} {1} {2} {3}">', VP_DS_SELECT_BOX, 'right', VP_DS_DROPPABLE, 'no-selection');
        tag.appendLine('</div>');  // VP_DS_SELECT_BOX
        tag.appendLine('</div>');  // VP_DS_SELECT_RIGHT
        tag.appendLine('</div>');  // VP_DS_SELECT_CONTAINER
        return tag.toString();
    }

    /**
     * Render column list box
     * @param {Array} colList 
     */
    DataSelector.prototype.renderColumnSelectionBox = function(colList) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0} {1} {2} {3}">', VP_DS_SELECT_BOX, 'left', VP_DS_DROPPABLE, 'no-selection');
        // get col data and make draggable items
        colList.forEach((col, idx) => {
            tag.appendFormatLine('<div class="{0} {1} {2}" data-idx="{3}" data-colname="{4}" data-dtype="{5}" data-code="{6}" title="{7}"><span>{8}</span></div>'
                                , VP_DS_SELECT_ITEM, 'select-col', VP_DS_DRAGGABLE, col.location, col.value, col.dtype, col.code, col.label + ': \n' + col.array, col.label);
        });
        tag.appendLine('</div>');  // VP_DS_SELECT_BOX
        return tag.toString();
    }

    /**
     * Render column slicing box
     * - slicing start/end with suggestInput
     * @param {Array} colList 
     */
    DataSelector.prototype.renderColumnSlicingBox = function(colList) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0}">', VP_DS_SLICING_BOX);
        tag.appendFormatLine('<label class="{0}">{1}</label>'
                                , '', 'Slice');
        // tag.appendFormatLine('<input type="text" class="{0} {1}" placeholder="{2}"/> : ', VP_DS_COL_SLICE_START, 'vp-input m', 'start');
        // tag.appendFormatLine('<input type="text" class="{0} {1}" placeholder="{2}"/>', VP_DS_COL_SLICE_END, 'vp-input m', 'end');
        var vpColStart = new vpSuggestInputText.vpSuggestInputText();
        vpColStart.addClass(VP_DS_COL_SLICE_START);
        vpColStart.addClass('vp-input m');
        vpColStart.setPlaceholder('start');
        vpColStart.setSuggestList(function() { return colList });
        vpColStart.setSelectEvent(function(value, item) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).attr('data-code', item.code);
            $(this.wrapSelector()).trigger('change');
        });
        vpColStart.setNormalFilter(false);

        var vpColEnd = new vpSuggestInputText.vpSuggestInputText();
        vpColEnd.addClass(VP_DS_COL_SLICE_END);
        vpColEnd.addClass('vp-input m');
        vpColEnd.setPlaceholder('end');
        vpColEnd.setSuggestList(function() { return colList });
        vpColEnd.setSelectEvent(function(value, item) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).attr('data-code', item.code);
            $(this.wrapSelector()).trigger('change');
        });
        vpColEnd.setNormalFilter(false);

        tag.appendLine(vpColStart.toTagString());
        tag.appendLine(vpColEnd.toTagString());
        tag.appendLine('</div>');
        return tag.toString();
    }

    /**
     * Render Row Condition List with columns
     * - column name
     * - operator
     * - condition string
     * - and/or connector between prev/next conditions
     * @param {Array} colList 
     */
    DataSelector.prototype.renderColumnConditionList = function(colList) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<table class="{0}">', VP_DS_CONDITION_TBL);
        tag.appendLine('<tr>');
        tag.appendLine('<td>');

        var varList = this.state.dataList;
        tag.appendLine(this.renderConditionVariableInput(varList, this.state.pandasObject, this.state.dataType));

        // tag.appendLine('<input type="text" class="vp-input m vp-col-list" placeholder="Column Name"/>');
        tag.appendLine(this.renderConditionColumnInput(colList));

        // tag.appendLine('<input type="text" class="vp-input s vp-oper-list" placeholder="Oper"/>');
        var vpOperSuggest = new vpSuggestInputText.vpSuggestInputText();
        vpOperSuggest.addClass('vp-input s vp-oper-list');
        vpOperSuggest.setPlaceholder("Oper");
        vpOperSuggest.setSuggestList(function() { return ['==', '!=', 'and', 'or', 'in', 'not in', '<', '<=', '>', '>=']; });
        vpOperSuggest.setSelectEvent(function(value) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).trigger('change');
        });
        vpOperSuggest.setNormalFilter(false);
        tag.appendLine(vpOperSuggest.toTagString());

        // use text
        tag.appendFormatLine('<label><input type="checkbox" class="{0}" title="{1}" checked/><span>{2}</span></label>'
                            , 'vp-cond-use-text', 'Uncheck it if you want to use variable or numeric values.', 'Text');

        tag.appendLine('<input class="vp-input m vp-condition" type="text" placeholder=""/>');
        tag.appendLine('<select class="vp-select s vp-oper-connect">');
        tag.appendLine('<option value="&">and</option>');
        tag.appendLine('<option value="|">or</option>');
        tag.appendLine('</select>');
        tag.appendLine('<div class="vp-icon-btn vp-del-col"></div>');
        tag.appendLine('</td>');
        tag.appendLine('</tr>');
        tag.appendLine('<tr>');
        tag.appendLine('<td colspan="4"><div class="vp-icon-btn vp-add-col"></i></td>');
        tag.appendLine('</tr>');
        tag.appendLine('</table>');
        return tag.toString();
    }

    DataSelector.prototype.renderConditionVariableInput = function(varList, defaultValue, defaultValuesType) {
        var vpVarSuggest = new vpSuggestInputText.vpSuggestInputText();
        vpVarSuggest.addClass('vp-input m vp-cond-var');
        vpVarSuggest.addAttribute('data-type', defaultValuesType);
        vpVarSuggest.setPlaceholder('Variable');
        vpVarSuggest.setSuggestList(function() { return varList; });
        vpVarSuggest.setValue(defaultValue);
        vpVarSuggest.setSelectEvent(function(value, item) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).attr('data-type', item.dtype);
            $(this.wrapSelector()).trigger('change');
        });
        vpVarSuggest.setNormalFilter(true);
        return vpVarSuggest.toTagString();
    }

    DataSelector.prototype.renderConditionColumnInput = function(colList) {
        var vpColSuggest = new vpSuggestInputText.vpSuggestInputText();
        vpColSuggest.addClass('vp-input m vp-col-list');
        vpColSuggest.setPlaceholder('Column Name');
        vpColSuggest.setSuggestList(function() { return colList });
        vpColSuggest.setSelectEvent(function(value, item) {
            $(this.wrapSelector()).val(value);
            $(this.wrapSelector()).attr('data-code', item.code);
            $(this.wrapSelector()).trigger('change');
        });
        vpColSuggest.setNormalFilter(false);
        return vpColSuggest.toTagString();
    }

    DataSelector.prototype.renderConditionCondInput = function(category) {
        var vpCondSuggest = new vpSuggestInputText.vpSuggestInputText();
        vpCondSuggest.addClass('vp-input m vp-condition');

        if (category && category.length > 0) {
            vpCondSuggest.setPlaceholder("Categorical Dtype");
            vpCondSuggest.setSuggestList(function() { return category; });
            vpCondSuggest.setSelectEvent(function(value) {
                $(this.wrapSelector()).val(value);
                $(this.wrapSelector()).trigger('change');
            });
            vpCondSuggest.setNormalFilter(false);
        } else {

        }
        return vpCondSuggest.toTagString();
    }

    /**
     * Render Data Tab Page
     * @param {String} renderedText 
     */
    DataSelector.prototype.renderDataPage = function(renderedText, isHtml = true) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0} {1}">', VP_DS_DATA_VIEW_BOX
                            , 'rendered_html'); // 'rendered_html' style from jupyter output area
        if (isHtml) {
            tag.appendLine(renderedText);
        } else {
            tag.appendFormatLine('<pre>{0}</pre>', renderedText);
        }
        tag.appendLine('</div>');
        return tag.toString();
    }

    

    ///////////////////////// render end //////////////////////////////////////////////////////

    ///////////////////////// load ///////////////////////////////////////////////////////////

    /**
     * Load Data Tab Page
     * - execute generated current code and get html text from jupyter kernel
     * - render data page with html text (msg.content.data['text/html'])
     */
    DataSelector.prototype.loadDataPage = function() {
        var that = this;

        var code = this.state.pandasObject;

        // if view all is not checked, get current code
        if (!this.state.viewAll) {
            // get current code
            code = this.generateCode();
        }
        // if not, get output of all data in selected pandasObject

        Jupyter.notebook.kernel.execute(
            code,
            {
                iopub: {
                    output: function(msg) {
                        if (msg.content.data) {
                            var htmlText = String(msg.content.data["text/html"]);
                            var codeText = String(msg.content.data["text/plain"]);
                            if (htmlText != 'undefined') {
                                $(that.wrapSelector('.' + VP_DS_DATA_VIEW_BOX)).replaceWith(function() {
                                    return that.renderDataPage(htmlText);
                                });
                            } else if (codeText != 'undefined') {
                                // plain text as code
                                $(that.wrapSelector('.' + VP_DS_DATA_VIEW_BOX)).replaceWith(function() {
                                    return that.renderDataPage(codeText, false);
                                });
                            } else {
                                $(that.wrapSelector('.' + VP_DS_DATA_VIEW_BOX)).replaceWith(function() {
                                    return that.renderDataPage('');
                                });
                            }
                        } else {
                            $(that.wrapSelector('.' + VP_DS_DATA_VIEW_BOX)).replaceWith(function() {
                                return that.renderDataPage('');
                            });
                        }
                    }
                }
            },
            { silent: false, store_history: true, stop_on_error: true }
        );
    }

    /**
     * Load pandasObject
     * - search available pandasObject list
     * - render on VP_DS_PANDAS_OBJECT
     */
     DataSelector.prototype.loadVariables = function() {
        var that = this;
        var types = []; //['DataFrame', 'Series'];
        pdGen.vp_searchVarList(types, function (result) {
            var varList = JSON.parse(result);
            varList = varList.map(function(v) {
                return { label: v.varName + ' (' + v.varType + ')', value: v.varName, dtype: v.varType };
            });

            that.state.dataList = varList;

            var pdTypes = ['DataFrame', 'Series'];
            var pdObjects = varList.filter(x => pdTypes.includes(x.dtype))

            // 1. Target Variable
            var prevValue = $(that.wrapSelector('.' + VP_DS_PANDAS_OBJECT)).val();
            var vpDfSuggest = new vpSuggestInputText.vpSuggestInputText();
            vpDfSuggest.addClass(VP_DS_PANDAS_OBJECT);
            vpDfSuggest.addClass('vp-input');
            vpDfSuggest.setPlaceholder('Select Object');
            vpDfSuggest.setSuggestList(function() { return pdObjects; });
            vpDfSuggest.setNormalFilter(false);
            vpDfSuggest.setSelectEvent(function(selectedValue, item) {
                // trigger change
                $(that.wrapSelector('.' + VP_DS_PANDAS_OBJECT)).val(selectedValue);
                that.state.dataType = item.dtype;
                that.reloadSubsetData();
            });
            $(that.wrapSelector('.' + VP_DS_PANDAS_OBJECT)).replaceWith(function() {
                return vpDfSuggest.toTagString();
            });
            $(that.wrapSelector('.' + VP_DS_PANDAS_OBJECT)).val(prevValue);
        });
    }

    DataSelector.prototype.loadSubsetType = function(dataType) {
        var that = this;
        $(this.wrapSelector('.' + VP_DS_SUBSET_TYPE)).replaceWith(function() {
            return that.renderSubsetType(dataType);
        });
    }

    DataSelector.prototype.loadRowColumnSubsetType = function(subsetType, timestamp = false) {
        var that = this;
        // get current subset type of row & column
        var rowSubset = this.state.rowType;
        var colSubset = this.state.colType;

        $(this.wrapSelector('.' + VP_DS_ROWTYPE)).replaceWith(function() {
            return that.renderRowSubsetType(subsetType, timestamp);
        });
        $(this.wrapSelector('.' + VP_DS_COLTYPE)).replaceWith(function() {
            return that.renderColumnSubsetType(subsetType);
        });

        $(this.wrapSelector('.' + VP_DS_ROWTYPE)).val(rowSubset);
        $(this.wrapSelector('.' + VP_DS_COLTYPE)).val(colSubset);

        var selectedRowType = $(this.wrapSelector('.' + VP_DS_ROWTYPE)).val();
        var selectedColType = $(this.wrapSelector('.' + VP_DS_COLTYPE)).val();

        if (selectedRowType != rowSubset) {
            $(this.wrapSelector('.' + VP_DS_ROWTYPE + ' option')).eq(0).prop('selected', true);
            this.state.rowType = $(this.wrapSelector('.' + VP_DS_ROWTYPE)).val();
        }
        if (selectedColType != colSubset) {
            $(this.wrapSelector('.' + VP_DS_COLTYPE + ' option')).eq(0).prop('selected', true);
            this.state.colType = $(this.wrapSelector('.' + VP_DS_COLTYPE)).val();
        }

        $(this.wrapSelector('.' + VP_DS_ROWTYPE)).trigger('change');
        $(this.wrapSelector('.' + VP_DS_COLTYPE)).trigger('change');


    }

    /**
     * Load Column List
     * - change state.columnList
     * - render column selection list
     * - render column slicing box
     * - render column condition list
     * @param {Array} columnList 
     */
    DataSelector.prototype.loadColumnList = function(columnList) {
        var that = this;
       
        // if iloc
        if (this.state.subsetType == 'iloc') {
            columnList = columnList.map(function(x) {
                return {
                    ...x,
                    label: x.location + '',
                    value: x.location + '',
                    code: x.location + '',
                };
            })
        }

        this.state.columnList = columnList;
        this.state.colPointer = { start: -1, end: -1 };

        // column selection
        $(this.wrapSelector('.' + VP_DS_SELECT_CONTAINER + '.select-col')).replaceWith(function() {
            return that.renderColumnIndexing(columnList);
        });

        // column slicing
        $(this.wrapSelector('.' + VP_DS_COLTYPE_BOX + ' .' + VP_DS_SLICING_BOX)).replaceWith(function() {
            return that.renderColumnSlicingBox(columnList);
        });

        // column condition
        $(this.wrapSelector('.' + VP_DS_CONDITION_TBL)).replaceWith(function() {
            return that.renderColumnConditionList(columnList);
        });
    }

    /**
     * Load Row List
     * - change state.rowList
     * - render row selection list
     * - render row slicing box
     * @param {Array} rowList 
     */
    DataSelector.prototype.loadRowList = function(rowList) {
        var that = this;

        // if iloc
        if (this.state.subsetType == 'iloc') {
            rowList = rowList.map(function(x) {
                return {
                    ...x,
                    label: x.location + '',
                    value: x.location + '',
                    code: x.location + '',
                };
            })
        }

        
        this.state.rowList = rowList;
        this.state.rowPointer = { start: -1, end: -1 };

        // is timestampindex ?
        if (rowList && rowList.length > 0 && rowList[0]['index_dtype'] == 'datetime64[ns]') {
            this.state.isTimestamp = true;
        } else {
            this.state.isTimestamp = false;
        }

        // row selection
        $(this.wrapSelector('.' + VP_DS_SELECT_CONTAINER + '.select-row')).replaceWith(function() {
            return that.renderRowIndexing(rowList);
        });

        // row slicing
        $(this.wrapSelector('.' + VP_DS_ROWTYPE_BOX + ' .' + VP_DS_SLICING_BOX)).replaceWith(function() {
            return that.renderRowSlicingBox(rowList);
        });

        this.loadRowColumnSubsetType(this.state.subsetType, this.state.isTimestamp);
    }

    ///////////////////////// load end ///////////////////////////////////////////////////////////

    /**
     * Bind Draggable to VP_DS_SELECT_ITEM
     * - bind draggable to VP_DS_DRAGGABLE
     * - bind droppable to VP_DS_DROPPABLE
     * @param {string} type 'row'/'col' 
     */
    DataSelector.prototype.bindDraggable = function(type) {
        var that = this;
        var draggableQuery = this.wrapSelector('.' + VP_DS_DRAGGABLE + '.select-' + type);
        var droppableQuery = this.wrapSelector('.select-' + type + ' .' + VP_DS_DROPPABLE);

        $(draggableQuery).draggable({
            // containment: '.select-' + type + ' .' + VP_DS_DROPPABLE,
            // appendTo: droppableQuery,
            // snap: '.' + VP_DS_DRAGGABLE,
            revert: 'invalid',
            cursor: 'pointer',
            connectToSortable: droppableQuery + '.right',
            // cursorAt: { bottom: 5, right: 5 },
            helper: function() {
                // selected items
                var widthString = parseInt($(this).outerWidth()) + 'px';
                var selectedTag = $(this).parent().find('.selected');
                if (selectedTag.length <= 0) {
                    selectedTag = $(this);
                }
                return $('<div></div>').append(selectedTag.clone().addClass('moving').css({ 
                    width: widthString, border: '0.25px solid #C4C4C4'
                }));
            }
        });

        $(droppableQuery).droppable({
            accept: draggableQuery,
            drop: function(event, ui) {
                var dropped = ui.draggable;
                var droppedOn = $(this);

                // is dragging on same droppable container?
                if (droppedOn.get(0) == $(dropped).parent().get(0)) {
                    
                    that.generateCode();
                    return ;
                }

                var dropGroup = $(dropped).parent().find('.selected:not(.moving)');
                // if nothing selected(as orange_text), use dragging item
                if (dropGroup.length <= 0) {
                    dropGroup = $(dropped);
                }
                $(dropGroup).detach().css({top:0, left:0}).appendTo(droppedOn);

                if ($(this).hasClass('right')) {
                    // add
                    $(dropGroup).addClass('added');
                } else {
                    // del
                    $(dropGroup).removeClass('added');
                    // sort
                    $(droppedOn).find('.' + VP_DS_SELECT_ITEM).sort(function(a, b) {
                        return ($(b).data('idx')) < ($(a).data('idx')) ? 1 : -1;
                    }).appendTo( $(droppedOn) );
                }
                // remove selection
                $(droppableQuery).find('.selected').removeClass('selected');
                that.state[type + 'Pointer'] = { start: -1, end: -1 };

                that.generateCode();
            },
            over: function(event, elem) {
            },
            out: function(event, elem) {
            }
        });

        
    }

    /**
     * Bind All Events
     * - open popup
     * - close popup
     * - pandasObject select/change
     * - use copy change
     * - subset type change
     * - tab change
     * - row/column subset type change
     * - row/column search value change
     * - row/column indexing add/del button click
     * - row/column slicing start/end value change
     * - condition values change
     * - condition add/del button click
     * - apply button click
     * - cancel button click
     */
    DataSelector.prototype.bindEvent = function() {
        var that = this;
        // open popup
        $(document).on('click', vpCommon.formatString('.{0}.{1}', VP_DS_BTN, this.uuid), function(event) {
            that.open();
        });
        
        // close popup
        $(document).on('click', this.wrapSelector('.' + VP_DS_CLOSE), function(event) {
            that.close();

            $(vpCommon.formatString('.{0}.{1}', VP_DS_BTN, this.uuid)).remove();
            // vpCommon.removeHeadScript("vpDataSelector");
        });

        // df selection/change
        $(document).on('select_suggest change', this.wrapSelector('.' + VP_DS_PANDAS_OBJECT), function(event) {
            var varName = $(that.wrapSelector('.' + VP_DS_PANDAS_OBJECT)).val();
            that.state.pandasObject = varName;
            that.state.rowList = [];
            that.state.columnList = [];
            that.state.rowPointer = { start: -1, end: -1 };
            that.state.colPointer = { start: -1, end: -1 };

            if (varName == '') {
                that.loadRowList([]);
                that.loadColumnList([]);
                that.generateCode();
                return;
            }

            that.loadSubsetType(that.state.dataType);
            
            if (that.state.dataType == 'DataFrame') {
                var colCode = vpCommon.formatString('_vp_print(_vp_get_columns_list({0}))', varName);
                // get result and load column list
                that.pageThis.kernelExecute(colCode, function(result) {
                    var colList = JSON.parse(result);
                    colList = colList.map(function(x) {
                        return {
                            ...x,
                            value: x.label,
                            code: x.value
                        };
                    });
                    that.loadColumnList(colList);
                    that.bindDraggable('col');
                    that.generateCode();
                });
                
                var rowCode = vpCommon.formatString('_vp_print(_vp_get_rows_list({0}))', varName);
                // get result and load column list
                that.pageThis.kernelExecute(rowCode, function(result) {
                    var rowList = JSON.parse(result);
                    rowList = rowList.map(function(x) {
                        return {
                            ...x,
                            value: x.label,
                            code: x.value
                        };
                    });
                    that.loadRowList(rowList);
                    that.bindDraggable('row');
                    that.generateCode();
                });

                // show column box
                $(that.wrapSelector('.' + VP_DS_TAB_PAGE_BOX + '.subset-column')).show();
            } else if (that.state.dataType == 'Series') {
                var rowCode = vpCommon.formatString('_vp_print(_vp_get_rows_list({0}))', varName);
                // get result and load column list
                that.pageThis.kernelExecute(rowCode, function(result) {
                    var rowList = JSON.parse(result);
                    rowList = rowList.map(function(x) {
                        return {
                            ...x,
                            value: x.label,
                            code: x.value
                        };
                    });
                    that.loadRowList(rowList);
                    that.bindDraggable('row');
                    that.generateCode();
                });

                that.loadColumnList([]);

                // hide to frame
                $(that.wrapSelector('.' + VP_DS_TO_FRAME)).parent().hide();
                // hide column box
                $(that.wrapSelector('.' + VP_DS_TAB_PAGE_BOX + '.subset-column')).hide();
            }

            // data page
            if (that.state.tabPage == 'data') {
                that.loadDataPage();
            }
        });

        // use copy
        $(document).on('change', this.wrapSelector('.' + VP_DS_USE_COPY), function(event) {
            var checked = $(this).prop('checked');
            that.state.useCopy = checked;

            that.generateCode();
        });
        
        // subset type select
        $(document).on('change', this.wrapSelector('.' + VP_DS_SUBSET_TYPE), function(event) {
            var subsetType = $(this).val();
            that.state.subsetType = subsetType;

            that.reloadSubsetData();
            // that.loadRowColumnSubsetType(subsetType, that.state.isTimestamp);
            // // data page
            // if (that.state.tabPage == 'data') {
            //     that.loadDataPage();
            // } else {
            //     that.generateCode();
            // }
        });

        // to frame
        $(document).on('change', this.wrapSelector('.' + VP_DS_TO_FRAME), function(event) {
            var checked = $(this).prop('checked');
            that.state.toFrame = checked;

            if (that.state.tabPage == 'data') {
                that.loadDataPage();
            } else {
                that.generateCode();
            }

        });

        // tab page select
        $(document).on('click', this.wrapSelector('.' + VP_DS_TAB_SELECTOR_BTN), function(event) {
            var page = $(this).attr('data-page');

            that.state.tabPage = page;

            // button toggle
            $(that.wrapSelector('.' + VP_DS_TAB_SELECTOR_BTN)).removeClass('selected');
            $(this).addClass('selected');

            // page toggle
            $(that.wrapSelector('.' + VP_DS_TAB_PAGE)).hide();
            if (page == 'subset') {
                // page: subset
                $(that.wrapSelector('.' + VP_DS_TAB_PAGE + '.subset')).show();
            } else {
                // page: data
                // loadDataPage
                that.loadDataPage();

                $(that.wrapSelector('.' + VP_DS_TAB_PAGE + '.data')).show();
            }
        });

        // view all
        $(document).on('change', this.wrapSelector('.' + VP_DS_DATA_VIEW_ALL), function(event) {
            var checked = $(this).prop('checked');
            that.state.viewAll = checked;

            that.loadDataPage();
        });
 
        // row type selector
        $(document).on('change', this.wrapSelector('.' + VP_DS_ROWTYPE), function(event) {
            var rowType = $(this).val();
            that.state.rowType = rowType;
            // hide
            $(that.wrapSelector('.' + VP_DS_ROWTYPE_BOX)).hide();
            $(that.wrapSelector('.' + VP_DS_ROWTYPE_BOX + '.' + rowType)).show();

            that.generateCode();
        });

        // column type selector
        $(document).on('change', this.wrapSelector('.' + VP_DS_COLTYPE), function(event) {
            var colType = $(this).val();
            that.state.colType = colType;
            // hide
            $(that.wrapSelector('.' + VP_DS_COLTYPE_BOX)).hide();
            $(that.wrapSelector('.' + VP_DS_COLTYPE_BOX + '.' + colType)).show();

            that.generateCode();
        });

        // row indexing - timestamp
        $(document).on('change', this.wrapSelector('.' + VP_DS_INDEXING_TIMESTAMP), function(event) {
            that.generateCode();
        });

        // item indexing - search index
        $(document).on('change', this.wrapSelector('.select-row .' + VP_DS_SELECT_SEARCH), function(event) {
            var searchValue = $(this).val();
            
            // filter added rows
            var addedTags = $(that.wrapSelector('.select-row .' + VP_DS_SELECT_RIGHT + ' .' + VP_DS_SELECT_ITEM + '.added'));
            var addedRowList = [];
            for (var i = 0; i < addedTags.length; i++) {
                var value = $(addedTags[i]).attr('data-rowname');
                addedRowList.push(value);
            }
            var filteredRowList = that.state.rowList.filter(x => x.value.toString().includes(searchValue) && !addedRowList.includes(x.value.toString()));

            // row indexing
            $(that.wrapSelector('.select-row .' + VP_DS_SELECT_BOX + '.left')).replaceWith(function() {
                return that.renderRowSelectionBox(filteredRowList);
            });

            // draggable
            that.bindDraggable('row');
        });

        // item indexing - search columns
        $(document).on('change', this.wrapSelector('.select-col .' + VP_DS_SELECT_SEARCH), function(event) {
            var searchValue = $(this).val();
            
            // filter added columns
            var addedTags = $(that.wrapSelector('.select-col .' + VP_DS_SELECT_RIGHT + ' .' + VP_DS_SELECT_ITEM + '.added'));
            var addedColumnList = [];
            for (var i = 0; i < addedTags.length; i++) {
                var value = $(addedTags[i]).attr('data-colname');
                addedColumnList.push(value);
            }
            var filteredColumnList = that.state.columnList.filter(x => x.value.includes(searchValue) && !addedColumnList.includes(x.value));

            // column indexing
            $(that.wrapSelector('.select-col .' + VP_DS_SELECT_BOX + '.left')).replaceWith(function() {
                return that.renderColumnSelectionBox(filteredColumnList);
            });

            // draggable
            that.bindDraggable('col');
        });

        // item indexing
        $(document).on('click', this.wrapSelector('.' + VP_DS_SELECT_ITEM), function(event) {
            var dataIdx = $(this).attr('data-idx');
            var idx = $(this).index();
            var itemType = $(this).hasClass('select-row')? 'row':'col';
            var added = $(this).hasClass('added'); // right side added item?

            var selector = '.select-' + itemType;

            // remove selection for select box on the other side
            if (added) {
                // remove selection for left side
                $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + '.select-' + itemType + ':not(.added)')).removeClass('selected');
                // set selector
                selector += '.added';
            } else {
                // remove selection for right(added) side
                $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + '.select-' + itemType + '.added')).removeClass('selected');
                // set selector
                selector += ':not(.added)';
            }

            if (that.keyboardManager.keyCheck.ctrlKey) {
                // multi-select
                that.state[itemType + 'Pointer'] = { start: idx, end: -1 };
                $(this).toggleClass('selected');
            } else if (that.keyboardManager.keyCheck.shiftKey) {
                // slicing
                var startIdx = that.state[itemType + 'Pointer'].start;
                
                if (startIdx == -1) {
                    // no selection
                    that.state[itemType + 'Pointer'] = { start: idx, end: -1 };
                } else if (startIdx > idx) {
                    // add selection from idx to startIdx
                    var tags = $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector));
                    for (var i = idx; i <= startIdx; i++) {
                        $(tags[i]).addClass('selected');
                    }
                    that.state[itemType + 'Pointer'] = { start: startIdx, end: idx };
                } else if (startIdx <= idx) {
                    // add selection from startIdx to idx
                    var tags = $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector));
                    for (var i = startIdx; i <= idx; i++) {
                        $(tags[i]).addClass('selected');
                    }
                    that.state[itemType + 'Pointer'] = { start: startIdx, end: idx };
                }
            } else {
                // single-select
                that.state[itemType + 'Pointer'] = { start: idx, end: -1 };
                // un-select others
                $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector)).removeClass('selected');
                // select this
                $(this).addClass('selected');
            }
        });

        // item indexing - add
        $(document).on('click', this.wrapSelector('.' + VP_DS_SELECT_ADD_BTN), function(event) {
            var itemType = $(this).hasClass('select-row')? 'row':'col';
            var selector = '.select-' + itemType + '.selected';

            $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector)).appendTo(
                $(that.wrapSelector('.select-' + itemType + ' .' + VP_DS_SELECT_BOX + '.right'))
            );
            $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector)).addClass('added');
            $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector)).removeClass('selected');
            that.state[itemType + 'Pointer'] = { start: -1, end: -1 };

            that.generateCode();
        });

        // item indexing - del
        $(document).on('click', this.wrapSelector('.' + VP_DS_SELECT_DEL_BTN), function(event) {
            var itemType = $(this).hasClass('select-row')? 'row':'col';
            var selector = '.select-' + itemType + '.selected';
            var targetBoxQuery = that.wrapSelector('.select-' + itemType + ' .' + VP_DS_SELECT_BOX + '.left');

            var selectedTag = $(that.wrapSelector('.' + VP_DS_SELECT_ITEM + selector));
            selectedTag.appendTo(
                $(targetBoxQuery)
            );
            // sort
            $(targetBoxQuery + ' .' + VP_DS_SELECT_ITEM).sort(function(a, b) {
                return ($(b).data('idx')) < ($(a).data('idx')) ? 1 : -1;
            }).appendTo(
                $(targetBoxQuery)
            );
            selectedTag.removeClass('added');
            selectedTag.removeClass('selected');
            that.state[itemType + 'Pointer'] = { start: -1, end: -1 };

            that.generateCode();
        });

        // row-column condition add
        $(document).on('click', this.wrapSelector('.vp-add-col'), function(event) {
            that.handleColumnAdd();

            that.generateCode();
        });

        // row-column condition delete
        $(document).on('click', this.wrapSelector('.vp-del-col'), function(event) {
            event.stopPropagation();
            
            var colList = $(that.wrapSelector('.' + VP_DS_CONDITION_TBL + ' tr td:not(:last)'));
            if (colList.length <= 1) {
                // clear
                // add new column
                that.handleColumnAdd();
            }

            // clear previous one
            $(this).parent().parent().remove();
            $(that.wrapSelector('.' + VP_DS_CONDITION_TBL + ' .vp-oper-connect:last')).hide();
            
            that.generateCode();
        });

        // typing on slicing
        $(document).on('change', this.wrapSelector('.slicing input[type="text"]'), function() {
            that.generateCode();
        });

        // typing on condition variable
        $(document).on('change', this.wrapSelector('.vp-ds-cond-tbl .vp-cond-var'), function() {
            var varType = $(this).attr('data-type');
            var colTag = $(this).parent().find('.vp-col-list');
            if (varType == 'DataFrame') {
                // pd Object selected
                var varName = $(this).val();
                // dataframe column search
                var colCode = vpCommon.formatString('_vp_print(_vp_get_columns_list({0}))', varName);
                // get result and load column list
                that.pageThis.kernelExecute(colCode, function(result) {
                    var colList = JSON.parse(result);
                    colList = colList.map(function(x) {
                        return {
                            ...x,
                            value: x.label,
                            code: x.value
                        };
                    });
                    $(colTag).replaceWith(function() {
                        return that.renderConditionColumnInput(colList);
                    });
                    $(colTag).attr('disabled', false);
                    that.generateCode();
                });
            } else {
                $(colTag).val('');
                $(colTag).attr('placeholder', '');
                $(colTag).attr('disabled', true);
            }
        });

        $(document).on('change', this.wrapSelector('.vp-ds-cond-tbl .vp-col-list'), function() {
            var varName = $(this).parent().find('.vp-cond-var').val();
            var colName = $(this).attr('data-code');

            var condTag = $(this).parent().find('.vp-condition');

            var code = vpCommon.formatString('_vp_print(_vp_get_column_category({0}, {1}))', varName, colName);
            // get result and load column list
            that.pageThis.kernelExecute(code, function(result) {
                var category = JSON.parse(result);
                $(condTag).replaceWith(function() {
                    return that.renderConditionCondInput(category);
                });
                that.generateCode();
            });

        });

        // use text
        $(document).on('change', this.wrapSelector('.vp-ds-cond-tbl .vp-cond-use-text'), function() {
            that.generateCode();
        });

        // typing on condition
        $(document).on('change', this.wrapSelector('.vp-ds-cond-tbl input[type="text"]'), function() {
            that.generateCode();
        });

        $(document).on('change', this.wrapSelector('.vp-ds-cond-tbl select'), function() {
            that.generateCode();
        });

        // DEPRECATED: now it will preview code on real time(on related value changing event)
        // preview code
        // $(document).on('click', this.wrapSelector('.' + VP_DS_BUTTON_PREVIEW), function(event) {
        //     var code = that.generateCode();
        // });

        // apply
        $(document).on('click', this.wrapSelector('.' + VP_DS_BUTTON_APPLY), function(event) {
            var code = that.generateCode();
            $(that.pageThis.wrapSelector('#' + that.targetId)).val(code);
            that.close();
        });

        // cancel
        $(document).on('click', this.wrapSelector('.' + VP_DS_BUTTON_CANCEL), function(event) {
            that.close();
        });

        ///////////////////////// FIXME: make it common //////////////////////////////////////
        this.keyboardManager = {
            keyCode : {
                ctrlKey: 17,
                cmdKey: 91,
                shiftKey: 16,
                altKey: 18,
                enter: 13
            },
            keyCheck : {
                ctrlKey: false,
                shiftKey: false
            }
        }
        $(document).keydown(function(e) {
            var keyCode = that.keyboardManager.keyCode;
            if (e.keyCode == keyCode.ctrlKey || e.keyCode == keyCode.cmdKey) {
                that.keyboardManager.keyCheck.ctrlKey = true;
            } 
            if (e.keyCode == keyCode.shiftKey) {
                that.keyboardManager.keyCheck.shiftKey = true;
            }
        }).keyup(function(e) {
            var keyCode = that.keyboardManager.keyCode;
            if (e.keyCode == keyCode.ctrlKey || e.keyCode == keyCode.cmdKey) {
                that.keyboardManager.keyCheck.ctrlKey = false;
            } 
            if (e.keyCode == keyCode.shiftKey) {
                that.keyboardManager.keyCheck.shiftKey = false;
            }
        });
    }

    /**
     * open popup
     */
    DataSelector.prototype.open = function() {
        // reload pandasObject on open
        this.loadVariables();

        $(vpCommon.formatString(".{0}.{1}", VP_DS, this.uuid)).show();
    }

    /**
     * close popup
     */
    DataSelector.prototype.close = function() {
        $(vpCommon.formatString(".{0}.{1}", VP_DS, this.uuid)).hide();
    }

    /**
     * Handle Adding Condition
     */
    DataSelector.prototype.handleColumnAdd = function() {
        var that = this;
        var clone = $(this.wrapSelector('.' + VP_DS_CONDITION_TBL + ' tr:first')).clone();

        clone.find('input').val('');
        clone.find('.vp-condition').attr({'placeholder': ''});

        clone.find('.vp-cond-var').replaceWith(function() {
            return that.renderConditionVariableInput(that.state.dataList, that.state.pandasObject, that.state.dataType);
        });
        clone.find('.vp-cond-var').val(this.state.pandasObject);

        // set column suggest input
        clone.find('.vp-col-list').replaceWith(function() {
            return that.renderConditionColumnInput(that.state.columnList);
        });

        // set use text default to true
        clone.find('.vp-cond-use-text').prop('checked', true);

        // set operater suggest input
        clone.find('.vp-oper-list').replaceWith(function() {
            var suggestInput = new vpSuggestInputText.vpSuggestInputText();
            suggestInput.addClass('vp-input s vp-oper-list');
            suggestInput.setPlaceholder("Oper");
            suggestInput.setSuggestList(function() { return ['==', '!=', 'and', 'or', 'in', 'not in', '<', '<=', '>', '>=']; });
            suggestInput.setSelectEvent(function(value) {
                $(this.wrapSelector()).val(value);
                $(this.wrapSelector()).trigger('change');
            });
            suggestInput.setNormalFilter(false);
            return suggestInput.toTagString();
        });

        // hide last connect operator
        clone.find('.vp-oper-connect').hide();
        // show connect operator right before last one
        $(this.wrapSelector('.' + VP_DS_CONDITION_TBL + ' .vp-oper-connect:last')).show();
        clone.insertBefore(this.wrapSelector('.' + VP_DS_CONDITION_TBL + ' tr:last'));
    }

    /**
     * Re-load subset data
     * - trigger dataframe change event
     */
    DataSelector.prototype.reloadSubsetData = function() {
        $(this.wrapSelector('.' + VP_DS_PANDAS_OBJECT)).trigger('select_suggest');
    }

    /**
     * Generate Code
     * - default: # PREVIEW CODE
     * - get 2 types of codes
     *  1) rowSelection - indexing/slicing/condition code
     *  2) colSelection - indexing/slicing code
     * - consider 3 types of subset frame
     *  1) subset - rowSelection & colSelection using 'indexing' type
     *  2) loc - subset type 'loc'
     *  3) iloc - subset type 'iloc'
     * - consider use copy option
     */
    DataSelector.prototype.generateCode = function() {
        var code = new sb.StringBuilder();

        // dataframe
        if (this.state.pandasObject == '') {
            $(this.wrapSelector('.' + VP_DS_PREVIEW)).text('# PREVIEW CODE');
            return '';
        }
        code.append(this.state.pandasObject);

        // row
        var rowSelection = new sb.StringBuilder();
        // depend on type
        if (this.state.rowType == 'indexing') {
            if (this.state.subsetType == 'subset' && this.state.isTimestamp) {
                var tsIndexing = $(this.wrapSelector('.' + VP_DS_INDEXING_TIMESTAMP)).val();
                if (tsIndexing != '') {
                    rowSelection.appendFormat("'{0}'", tsIndexing);
                }
            } else {
                var rowTags = $(this.wrapSelector('.' + VP_DS_SELECT_ITEM + '.select-row.added:not(.moving)'));
                if (rowTags.length > 0) {
                    var rowList = [];
                    for (var i = 0; i < rowTags.length; i++) {
                        var rowValue = $(rowTags[i]).attr('data-code');
                        if (rowValue) {
                            rowList.push(rowValue);
                        }
                    }
                    rowSelection.appendFormat('[{0}]', rowList.toString());
                } else {
                    rowSelection.append(':');
                }
            }
        } else if (this.state.rowType == 'slicing') {
            var start = $(this.wrapSelector('.' + VP_DS_ROW_SLICE_START)).attr('data-code');
            var end = $(this.wrapSelector('.' + VP_DS_ROW_SLICE_END)).attr('data-code');
            rowSelection.appendFormat('{0}:{1}', start?start:'', end?end:'');
        } else if (this.state.rowType == 'condition') {
            // condition
            var condList = $(this.wrapSelector('.' + VP_DS_CONDITION_TBL + ' tr td:not(:last)'));
            var useCondition = false;
            for (var i = 0; i < condList.length; i++) {
                var colTag = $(condList[i]);
                var varName = colTag.find('.vp-cond-var').val();
                var varType = colTag.find('.vp-cond-var').attr('data-type');
                var colName = colTag.find('.vp-col-list').attr('data-code');
                colName = colName? colName: '';
                var oper = colTag.find('.vp-oper-list').val();
                var useText = colTag.find('.vp-cond-use-text').prop('checked');
                var cond = colTag.find('.vp-condition').val();
                var connector = i > 0? $(condList[i- 1]).find('.vp-oper-connect').val() : undefined;

                // if no variable selected, pass
                if (varName == "") continue;
                if (useCondition) {
                    rowSelection.append(connector);
                }

                if (varType == 'DataFrame') {
                    rowSelection.appendFormat('({0}', varName);
                    colName && rowSelection.appendFormat('[{0}]', colName);
                    oper && rowSelection.appendFormat(' {0}', oper);
                    if (cond) {
                        // condition value as text
                        if (useText) {
                            rowSelection.appendFormat(" '{0}'", cond);
                        } else {
                            rowSelection.appendFormat(" {0}", cond);
                        }
                    }
                    rowSelection.append(')');
                } else {
                    rowSelection.appendFormat('({0}', varName);
                    oper && rowSelection.appendFormat(' {0}', oper);
                    if (cond) {
                        // condition value as text
                        if (useText) {
                            rowSelection.appendFormat(" '{0}'", cond);
                        } else {
                            rowSelection.appendFormat(" {0}", cond);
                        }
                    }
                    rowSelection.append(')');
                }
                useCondition = true;
            }
        } else {
            rowSelection.append(':');
        }

        

        // columns
        // selected colList
        var colSelection = new sb.StringBuilder();

        // hide to frame
        $(this.wrapSelector('.' + VP_DS_TO_FRAME)).parent().hide();
        if (this.state.dataType == 'DataFrame') {
            if (this.state.colType == 'indexing') {
                var colTags = $(this.wrapSelector('.' + VP_DS_SELECT_ITEM + '.select-col.added:not(.moving)'));
                if (colTags.length > 0) {
                    var colList = [];
                    for (var i = 0; i < colTags.length; i++) {
                        var colValue = $(colTags[i]).attr('data-code');
                        if (colValue) {
                            colList.push(colValue);
                        }
                    }

                    // hide/show to frame
                    if (colList.length == 1) {
                        $(this.wrapSelector('.' + VP_DS_TO_FRAME)).parent().show();

                        // to frame
                        if (this.state.toFrame) {
                            colSelection.appendFormat('[{0}]', colList.toString());
                        } else {
                            colSelection.appendFormat('{0}', colList.toString());
                        }
                    } else {
                        colSelection.appendFormat('[{0}]', colList.toString());
                    }
                    
                } else {
                    colSelection.append(':');
                }
            } else if (this.state.colType == 'slicing') {
                var start = $(this.wrapSelector('.' + VP_DS_COL_SLICE_START)).attr('data-code');
                var end = $(this.wrapSelector('.' + VP_DS_COL_SLICE_END)).attr('data-code');
                colSelection.appendFormat('{0}:{1}', start? start: '', end? end: '');
            }
        }

        // use simple selection
        if (this.state.subsetType == 'subset') {
            if (rowSelection.toString() != ':' && rowSelection.toString() != '') {
                code.appendFormat('[{0}]', rowSelection.toString());
            }
            if (colSelection.toString() != ':' && colSelection.toString() != '') {
                code.appendFormat('[{0}]', colSelection.toString());
            }
        } else if (this.state.subsetType == 'loc') {
            code.appendFormat('.loc[{0}, {1}]', rowSelection.toString(), colSelection.toString());
        } else if (this.state.subsetType == 'iloc') {
            code.appendFormat('.iloc[{0}, {1}]', rowSelection.toString(), colSelection.toString());
        }

        // use copy
        if (this.state.useCopy) {
            code.append('.copy()');
        }

        // preview code
        $(this.wrapSelector('.' + VP_DS_PREVIEW)).text(code.toString());

        return code.toString();
    }

    return DataSelector
});