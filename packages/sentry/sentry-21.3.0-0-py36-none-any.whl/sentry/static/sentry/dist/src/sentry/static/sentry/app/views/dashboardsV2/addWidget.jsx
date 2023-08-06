import { __makeTemplateObject } from "tslib";
import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import styled from '@emotion/styled';
import { IconAdd } from 'app/icons';
import WidgetWrapper from './widgetWrapper';
export var ADD_WIDGET_BUTTON_DRAG_ID = 'add-widget-button';
var initialStyles = {
    x: 0,
    y: 0,
    scaleX: 1,
    scaleY: 1,
};
function AddWidget(props) {
    var onClick = props.onClick;
    var _a = useSortable({
        disabled: true,
        id: ADD_WIDGET_BUTTON_DRAG_ID,
        transition: null,
    }), setNodeRef = _a.setNodeRef, transform = _a.transform;
    return (<WidgetWrapper key="add" ref={setNodeRef} displayType="big_number" layoutId={ADD_WIDGET_BUTTON_DRAG_ID} style={{ originX: 0, originY: 0 }} animate={transform
        ? {
            x: transform.x,
            y: transform.y,
            scaleX: (transform === null || transform === void 0 ? void 0 : transform.scaleX) && transform.scaleX <= 1 ? transform.scaleX : 1,
            scaleY: (transform === null || transform === void 0 ? void 0 : transform.scaleY) && transform.scaleY <= 1 ? transform.scaleY : 1,
        }
        : initialStyles} transition={{
        duration: 0.25,
    }}>
      <AddWidgetWrapper key="add" data-test-id="widget-add" onClick={onClick}>
        <IconAdd size="lg" isCircled color="inactive"/>
      </AddWidgetWrapper>
    </WidgetWrapper>);
}
var AddWidgetWrapper = styled('a')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  height: 110px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  width: 100%;\n  height: 110px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
export default AddWidget;
var templateObject_1;
//# sourceMappingURL=addWidget.jsx.map