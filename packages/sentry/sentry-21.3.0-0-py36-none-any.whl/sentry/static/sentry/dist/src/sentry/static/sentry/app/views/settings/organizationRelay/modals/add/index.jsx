import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import List from 'app/components/list';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import ModalManager from '../modalManager';
import Item from './item';
import Terminal from './terminal';
var Add = /** @class */ (function (_super) {
    __extends(Add, _super);
    function Add() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Add.prototype.getTitle = function () {
        return t('Register Key');
    };
    Add.prototype.getBtnSaveLabel = function () {
        return t('Register');
    };
    Add.prototype.getData = function () {
        var savedRelays = this.props.savedRelays;
        var trustedRelays = __spread(savedRelays, [this.state.values]);
        return { trustedRelays: trustedRelays };
    };
    Add.prototype.getContent = function () {
        return (<StyledList symbol="colored-numeric">
        <Item title={tct('Initialize the configuration. [link: Learn how]', {
            link: (<ExternalLink href="https://docs.sentry.io/product/relay/getting-started/#initializing-configuration"/>),
        })} subtitle={t('Within your terminal:')}>
          <Terminal command="relay config init"/>
        </Item>
        <Item title={tct('Go to the file [jsonFile: credentials.json] to find the public key and enter it below.', {
            jsonFile: (<ExternalLink href="https://docs.sentry.io/product/relay/getting-started/#registering-relay-with-sentry"/>),
        })}>
          {_super.prototype.getForm.call(this)}
        </Item>
      </StyledList>);
    };
    return Add;
}(ModalManager));
export default Add;
var StyledList = styled(List)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(3));
var templateObject_1;
//# sourceMappingURL=index.jsx.map