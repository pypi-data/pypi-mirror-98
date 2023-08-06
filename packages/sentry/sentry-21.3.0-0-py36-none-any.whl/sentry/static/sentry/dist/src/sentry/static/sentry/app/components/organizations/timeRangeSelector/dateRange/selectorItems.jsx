import React from 'react';
import RelativeSelector from 'app/components/organizations/timeRangeSelector/dateRange/relativeSelector';
import SelectorItem from 'app/components/organizations/timeRangeSelector/dateRange/selectorItem';
import { t } from 'app/locale';
var SelectorItems = function (_a) {
    var shouldShowRelative = _a.shouldShowRelative, shouldShowAbsolute = _a.shouldShowAbsolute, handleSelectRelative = _a.handleSelectRelative, handleAbsoluteClick = _a.handleAbsoluteClick, relativeSelected = _a.relativeSelected, isAbsoluteSelected = _a.isAbsoluteSelected;
    return (<React.Fragment>
    {shouldShowRelative && (<RelativeSelector onClick={handleSelectRelative} selected={relativeSelected}/>)}
    {shouldShowAbsolute && (<SelectorItem onClick={handleAbsoluteClick} value="absolute" label={t('Absolute date')} selected={isAbsoluteSelected} last/>)}
  </React.Fragment>);
};
export default SelectorItems;
//# sourceMappingURL=selectorItems.jsx.map