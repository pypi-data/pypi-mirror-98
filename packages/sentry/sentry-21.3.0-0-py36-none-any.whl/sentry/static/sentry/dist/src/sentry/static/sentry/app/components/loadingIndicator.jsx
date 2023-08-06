import React from 'react';
import { withProfiler } from '@sentry/react';
import classNames from 'classnames';
function renderLogoSpinner() {
    // If you update this also its sibling in sentry/bases/react.html and app/index.html
    return (<svg width="90" height="90" viewBox="0 0 90 90">
      <defs>
        <path id="loading-logo" fill="none" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" d="M8.07 50.083c-1.744 2.885-3.192 5.403-4.344 7.556-1.729 3.228.522 6.041 3.335 6.041h18.86c.056-10.925-6.902-18.96-12.867-22.226 1.9-3.173 5.12-8.986 6.313-10.984 12.02 6.966 19.14 19.803 19.14 33.21 4.01.027 8.422 0 12.638 0 .01-16.823-8.633-34.304-25.512-44.004 4.289-7.375 7.02-12.354 8.532-14.733 1.512-2.378 5.214-2.395 6.656 0 1.443 2.395 28.98 50.16 30.451 52.696 1.471 2.536.034 6.041-3.751 6.041h-6.789"/>
      </defs>
      <use x="5" y="5" xlinkHref="#loading-logo" className="logo-spin-1"/>
      <use x="5" y="5" xlinkHref="#loading-logo" className="logo-spin-0"/>
    </svg>);
}
function LoadingIndicator(props) {
    var hideMessage = props.hideMessage, mini = props.mini, triangle = props.triangle, overlay = props.overlay, dark = props.dark, children = props.children, finished = props.finished, className = props.className, style = props.style, relative = props.relative, size = props.size, hideSpinner = props.hideSpinner;
    var cx = classNames(className, {
        overlay: overlay,
        dark: dark,
        loading: true,
        mini: mini,
        triangle: triangle,
    });
    var loadingCx = classNames({
        relative: relative,
        'loading-indicator': true,
        'load-complete': finished,
    });
    var loadingStyle = {};
    if (size) {
        loadingStyle = {
            width: size,
            height: size,
        };
    }
    return (<div className={cx} style={style}>
      {!hideSpinner && (<div className={loadingCx} style={loadingStyle}>
          {triangle && renderLogoSpinner()}
          {finished ? <div className="checkmark draw" style={style}/> : null}
        </div>)}
      {!hideMessage && <div className="loading-message">{children}</div>}
    </div>);
}
export default withProfiler(LoadingIndicator, {
    includeUpdates: false,
});
//# sourceMappingURL=loadingIndicator.jsx.map