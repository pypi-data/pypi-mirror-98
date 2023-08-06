import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import NotAvailable from 'app/components/notAvailable';
import space from 'app/styles/space';
function List(_a) {
    var items = _a.items, className = _a.className;
    if (!items.length) {
        return <NotAvailable />;
    }
    return <Wrapper className={className}>{items}</Wrapper>;
}
export default List;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(2), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=list.jsx.map