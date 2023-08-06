import React from 'react';
import { t } from 'app/locale';
import Redaction from './redaction';
// If you find yourself modifying this component to fix some tooltip bug,
// consider that `meta` is not properly passed into this component in the
// first place. It's much more likely that `withMeta` is buggy or improperly
// used than that this component has a bug.
var ValueElement = function (_a) {
    var _b, _c;
    var value = _a.value, meta = _a.meta;
    if (value && meta) {
        return <Redaction>{value}</Redaction>;
    }
    if ((_b = meta === null || meta === void 0 ? void 0 : meta.err) === null || _b === void 0 ? void 0 : _b.length) {
        return (<Redaction withoutBackground>
        <i>{"<" + t('invalid') + ">"}</i>
      </Redaction>);
    }
    if ((_c = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _c === void 0 ? void 0 : _c.length) {
        return (<Redaction>
        <i>{"<" + t('redacted') + ">"}</i>
      </Redaction>);
    }
    if (React.isValidElement(value)) {
        return value;
    }
    return (<React.Fragment>
      {typeof value === 'object' ? JSON.stringify(value) : value}
    </React.Fragment>);
};
export default ValueElement;
//# sourceMappingURL=valueElement.jsx.map