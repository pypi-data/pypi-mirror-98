import { __extends } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import InputField from 'app/views/settings/components/forms/inputField';
import SelectField from 'app/views/settings/components/forms/selectField';
var CustomIgnoreCountModal = /** @class */ (function (_super) {
    __extends(CustomIgnoreCountModal, _super);
    function CustomIgnoreCountModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            count: 100,
            window: null,
        };
        _this.handleSubmit = function () {
            var _a;
            var _b = _this.state, count = _b.count, window = _b.window;
            var _c = _this.props, countName = _c.countName, windowName = _c.windowName;
            var statusDetails = (_a = {}, _a[countName] = count, _a);
            if (window) {
                statusDetails[windowName] = window;
            }
            _this.props.onSelected(statusDetails);
            _this.props.closeModal();
        };
        _this.handleChange = function (name, value) {
            var _a;
            _this.setState((_a = {}, _a[name] = value, _a));
        };
        return _this;
    }
    CustomIgnoreCountModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Footer = _a.Footer, Body = _a.Body, countLabel = _a.countLabel, label = _a.label, closeModal = _a.closeModal, windowChoices = _a.windowChoices;
        var _b = this.state, count = _b.count, window = _b.window;
        return (<React.Fragment>
        <Header>
          <h4>{label}</h4>
        </Header>
        <Body>
          <InputField inline={false} flexibleControlStateSize stacked label={countLabel} name="count" type="number" value={count} onChange={function (val) { return _this.handleChange('count', Number(val)); }} required placeholder={t('e.g. 100')}/>
          <SelectField inline={false} flexibleControlStateSize stacked label={t('Time window')} value={window} name="window" onChange={function (val) { return _this.handleChange('window', val); }} choices={windowChoices} placeholder={t('e.g. per hour')} allowClear help={t('(Optional) If supplied, this rule will apply as a rate of change.')}/>
        </Body>
        <Footer>
          <ButtonBar gap={1}>
            <Button type="button" onClick={closeModal}>
              {t('Cancel')}
            </Button>
            <Button type="button" priority="primary" onClick={this.handleSubmit}>
              {t('Ignore')}
            </Button>
          </ButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return CustomIgnoreCountModal;
}(React.Component));
export default CustomIgnoreCountModal;
//# sourceMappingURL=customIgnoreCountModal.jsx.map