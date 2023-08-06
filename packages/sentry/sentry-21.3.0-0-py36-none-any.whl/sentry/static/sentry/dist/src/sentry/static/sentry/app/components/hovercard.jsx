import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import { Manager, Popper, Reference } from 'react-popper';
import { keyframes } from '@emotion/core';
import styled from '@emotion/styled';
import classNames from 'classnames';
import { fadeIn } from 'app/styles/animations';
import space from 'app/styles/space';
import { domId } from 'app/utils/domId';
var VALID_DIRECTIONS = ['top', 'bottom', 'left', 'right'];
var Hovercard = /** @class */ (function (_super) {
    __extends(Hovercard, _super);
    function Hovercard(args) {
        var _this = _super.call(this, args) || this;
        _this.state = {
            visible: false,
        };
        _this.hoverWait = null;
        _this.handleToggleOn = function () { return _this.toggleHovercard(true); };
        _this.handleToggleOff = function () { return _this.toggleHovercard(false); };
        _this.toggleHovercard = function (visible) {
            var displayTimeout = _this.props.displayTimeout;
            if (_this.hoverWait) {
                clearTimeout(_this.hoverWait);
            }
            _this.hoverWait = window.setTimeout(function () { return _this.setState({ visible: visible }); }, displayTimeout);
        };
        var portal = document.getElementById('hovercard-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'hovercard-portal');
            document.body.appendChild(portal);
        }
        _this.portalEl = portal;
        _this.tooltipId = domId('hovercard-');
        _this.scheduleUpdate = null;
        return _this;
    }
    Hovercard.prototype.componentDidUpdate = function (prevProps) {
        var _a;
        var _b = this.props, body = _b.body, header = _b.header;
        if (body !== prevProps.body || header !== prevProps.header) {
            // We had a problem with popper not recalculating position when body/header changed while hovercard still opened.
            // This can happen for example when showing a loading spinner in a hovercard and then changing it to the actual content once fetch finishes.
            (_a = this.scheduleUpdate) === null || _a === void 0 ? void 0 : _a.call(this);
        }
    };
    Hovercard.prototype.render = function () {
        var _this = this;
        var _a = this.props, bodyClassName = _a.bodyClassName, containerClassName = _a.containerClassName, className = _a.className, header = _a.header, body = _a.body, position = _a.position, show = _a.show, tipColor = _a.tipColor, offset = _a.offset, modifiers = _a.modifiers;
        // Maintain the hovercard class name for BC with less styles
        var cx = classNames('hovercard', className);
        var popperModifiers = __assign({ hide: {
                enabled: false,
            }, preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            } }, (modifiers || {}));
        var visible = show !== undefined ? show : this.state.visible;
        var hoverProps = show !== undefined
            ? {}
            : { onMouseEnter: this.handleToggleOn, onMouseLeave: this.handleToggleOff };
        return (<Manager>
        <Reference>
          {function (_a) {
            var ref = _a.ref;
            return (<span ref={ref} aria-describedby={_this.tooltipId} className={containerClassName} {...hoverProps}>
              {_this.props.children}
            </span>);
        }}
        </Reference>
        {visible &&
            (header || body) &&
            ReactDOM.createPortal(<Popper placement={position} modifiers={popperModifiers}>
              {function (_a) {
                var ref = _a.ref, style = _a.style, placement = _a.placement, arrowProps = _a.arrowProps, scheduleUpdate = _a.scheduleUpdate;
                _this.scheduleUpdate = scheduleUpdate;
                return (<StyledHovercard id={_this.tooltipId} visible={visible} ref={ref} style={style} placement={placement} offset={offset} className={cx} {...hoverProps}>
                    {header && <Header>{header}</Header>}
                    {body && <Body className={bodyClassName}>{body}</Body>}
                    <HovercardArrow ref={arrowProps.ref} style={arrowProps.style} placement={placement} tipColor={tipColor}/>
                  </StyledHovercard>);
            }}
            </Popper>, this.portalEl)}
      </Manager>);
    };
    Hovercard.defaultProps = {
        displayTimeout: 100,
        position: 'top',
    };
    return Hovercard;
}(React.Component));
// Slide in from the same direction as the placement
// so that the card pops into place.
var slideIn = function (p) { return keyframes(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  from {\n    ", "\n    ", "\n    ", "\n    ", "\n  }\n  to {\n    ", "\n    ", "\n    ", "\n    ", "\n  }\n"], ["\n  from {\n    ", "\n    ", "\n    ", "\n    ", "\n  }\n  to {\n    ", "\n    ", "\n    ", "\n    ", "\n  }\n"])), p.placement === 'top' ? 'top: -10px;' : '', p.placement === 'bottom' ? 'top: 10px;' : '', p.placement === 'left' ? 'left: -10px;' : '', p.placement === 'right' ? 'left: 10px;' : '', p.placement === 'top' ? 'top: 0;' : '', p.placement === 'bottom' ? 'top: 0;' : '', p.placement === 'left' ? 'left: 0;' : '', p.placement === 'right' ? 'left: 0;' : ''); };
var getTipDirection = function (p) {
    return VALID_DIRECTIONS.includes(p.placement) ? p.placement : 'top';
};
var getOffset = function (p) { var _a; return (_a = p.offset) !== null && _a !== void 0 ? _a : space(2); };
var StyledHovercard = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-radius: ", ";\n  text-align: left;\n  padding: 0;\n  line-height: 1;\n  /* Some hovercards overlap the toplevel header and sidebar, and we need to appear on top */\n  z-index: ", ";\n  white-space: initial;\n  color: ", ";\n  border: 1px solid ", ";\n  background: ", ";\n  background-clip: padding-box;\n  box-shadow: 0 0 35px 0 rgba(67, 62, 75, 0.2);\n  width: 295px;\n\n  /* The hovercard may appear in different contexts, don't inherit fonts */\n  font-family: ", ";\n\n  position: absolute;\n  visibility: ", ";\n\n  animation: ", " 100ms, ", " 100ms ease-in-out;\n  animation-play-state: ", ";\n\n  /* Offset for the arrow */\n  ", ";\n  ", ";\n  ", ";\n  ", ";\n"], ["\n  border-radius: ", ";\n  text-align: left;\n  padding: 0;\n  line-height: 1;\n  /* Some hovercards overlap the toplevel header and sidebar, and we need to appear on top */\n  z-index: ", ";\n  white-space: initial;\n  color: ", ";\n  border: 1px solid ", ";\n  background: ", ";\n  background-clip: padding-box;\n  box-shadow: 0 0 35px 0 rgba(67, 62, 75, 0.2);\n  width: 295px;\n\n  /* The hovercard may appear in different contexts, don't inherit fonts */\n  font-family: ", ";\n\n  position: absolute;\n  visibility: ", ";\n\n  animation: ", " 100ms, ", " 100ms ease-in-out;\n  animation-play-state: ", ";\n\n  /* Offset for the arrow */\n  ", ";\n  ", ";\n  ", ";\n  ", ";\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.zIndex.hovercard; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.text.family; }, function (p) { return (p.visible ? 'visible' : 'hidden'); }, fadeIn, slideIn, function (p) { return (p.visible ? 'running' : 'paused'); }, function (p) { return (p.placement === 'top' ? "margin-bottom: " + getOffset(p) : ''); }, function (p) { return (p.placement === 'bottom' ? "margin-top: " + getOffset(p) : ''); }, function (p) { return (p.placement === 'left' ? "margin-right: " + getOffset(p) : ''); }, function (p) { return (p.placement === 'right' ? "margin-left: " + getOffset(p) : ''); });
var Header = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", ";\n  font-weight: 600;\n  word-wrap: break-word;\n  padding: ", ";\n"], ["\n  font-size: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", ";\n  font-weight: 600;\n  word-wrap: break-word;\n  padding: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadiusTop; }, space(1.5));
var Body = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n  min-height: 30px;\n"], ["\n  padding: ", ";\n  min-height: 30px;\n"])), space(2));
var HovercardArrow = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  width: 20px;\n  height: 20px;\n  z-index: -1;\n\n  ", ";\n  ", ";\n  ", ";\n  ", ";\n\n  &::before,\n  &::after {\n    content: '';\n    margin: auto;\n    position: absolute;\n    display: block;\n    width: 0;\n    height: 0;\n    top: 0;\n    left: 0;\n  }\n\n  /* before element is the hairline border, it is repositioned for each orientation */\n  &::before {\n    top: 1px;\n    border: 10px solid transparent;\n    border-", "-color: ", ";\n\n    ", ";\n    ", ";\n    ", ";\n  }\n  &::after {\n    border: 10px solid transparent;\n    border-", "-color: ", ";\n  }\n"], ["\n  position: absolute;\n  width: 20px;\n  height: 20px;\n  z-index: -1;\n\n  ", ";\n  ", ";\n  ", ";\n  ", ";\n\n  &::before,\n  &::after {\n    content: '';\n    margin: auto;\n    position: absolute;\n    display: block;\n    width: 0;\n    height: 0;\n    top: 0;\n    left: 0;\n  }\n\n  /* before element is the hairline border, it is repositioned for each orientation */\n  &::before {\n    top: 1px;\n    border: 10px solid transparent;\n    border-", "-color: ", ";\n\n    ", ";\n    ", ";\n    ", ";\n  }\n  &::after {\n    border: 10px solid transparent;\n    border-", "-color: ",
    ";\n  }\n"])), function (p) { return (p.placement === 'top' ? 'bottom: -20px; left: 0' : ''); }, function (p) { return (p.placement === 'bottom' ? 'top: -20px; left: 0' : ''); }, function (p) { return (p.placement === 'left' ? 'right: -20px' : ''); }, function (p) { return (p.placement === 'right' ? 'left: -20px' : ''); }, getTipDirection, function (p) { return p.tipColor || p.theme.border; }, function (p) { return (p.placement === 'bottom' ? 'top: -1px' : ''); }, function (p) { return (p.placement === 'left' ? 'top: 0; left: 1px;' : ''); }, function (p) { return (p.placement === 'right' ? 'top: 0; left: -1px' : ''); }, getTipDirection, function (p) {
    return p.tipColor || (p.placement === 'bottom' ? p.theme.backgroundSecondary : p.theme.white);
});
export { Body, Header, Hovercard };
export default Hovercard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=hovercard.jsx.map