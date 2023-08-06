import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
var WidgetWrapper = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  /* Min-width prevents grid items from stretching the grid */\n  min-width: 200px;\n  touch-action: manipulation;\n\n  ", ";\n"], ["\n  position: relative;\n  /* Min-width prevents grid items from stretching the grid */\n  min-width: 200px;\n  touch-action: manipulation;\n\n  ",
    ";\n"])), function (p) {
    switch (p.displayType) {
        case 'big_number':
            return 'grid-area: span 1 / span 1;';
        default:
            return 'grid-area: span 2 / span 2;';
    }
});
export default WidgetWrapper;
var templateObject_1;
//# sourceMappingURL=widgetWrapper.jsx.map