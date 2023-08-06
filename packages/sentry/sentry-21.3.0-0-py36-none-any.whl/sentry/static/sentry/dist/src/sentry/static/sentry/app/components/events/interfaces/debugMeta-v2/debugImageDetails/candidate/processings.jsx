import React from 'react';
import NotAvailable from 'app/components/notAvailable';
import { CandidateDownloadStatus, } from 'app/types/debugImage';
import ProcessingItem from '../../processing/item';
import ProcessingList from '../../processing/list';
import ProcessingIcon from './processingIcon';
function Processings(_a) {
    var candidate = _a.candidate;
    var items = [];
    if (candidate.download.status !== CandidateDownloadStatus.OK &&
        candidate.download.status !== CandidateDownloadStatus.DELETED) {
        return <NotAvailable />;
    }
    var _b = candidate, debug = _b.debug, unwind = _b.unwind;
    if (debug) {
        items.push(<ProcessingItem key="symbolication" type="symbolication" icon={<ProcessingIcon processingInfo={debug}/>}/>);
    }
    if (unwind) {
        items.push(<ProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<ProcessingIcon processingInfo={unwind}/>}/>);
    }
    return <ProcessingList items={items}/>;
}
export default Processings;
//# sourceMappingURL=processings.jsx.map