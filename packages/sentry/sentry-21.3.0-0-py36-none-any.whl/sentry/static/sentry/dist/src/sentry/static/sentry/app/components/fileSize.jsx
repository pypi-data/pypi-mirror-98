import React from 'react';
import { formatBytes } from 'app/utils';
import getDynamicText from 'app/utils/getDynamicText';
function FileSize(props) {
    var className = props.className, bytes = props.bytes;
    return (<span className={className}>
      {getDynamicText({ value: formatBytes(bytes), fixed: 'xx KB' })}
    </span>);
}
export default FileSize;
//# sourceMappingURL=fileSize.jsx.map