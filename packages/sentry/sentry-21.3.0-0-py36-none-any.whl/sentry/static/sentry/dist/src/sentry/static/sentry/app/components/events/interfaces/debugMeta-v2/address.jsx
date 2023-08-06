import { __read } from "tslib";
import React from 'react';
import { formatAddress, getImageRange } from 'app/components/events/interfaces/utils';
var IMAGE_ADDR_LEN = 12;
function Address(_a) {
    var image = _a.image;
    var _b = __read(getImageRange(image), 2), startAddress = _b[0], endAddress = _b[1];
    if (startAddress && endAddress) {
        return (<React.Fragment>
        <span>{formatAddress(startAddress, IMAGE_ADDR_LEN)}</span>
        {' \u2013 '}
        <span>{formatAddress(endAddress, IMAGE_ADDR_LEN)}</span>
      </React.Fragment>);
    }
    return null;
}
export default Address;
//# sourceMappingURL=address.jsx.map