// Candidate Processing Info
export var CandidateProcessingStatus;
(function (CandidateProcessingStatus) {
    CandidateProcessingStatus["OK"] = "ok";
    CandidateProcessingStatus["MALFORMED"] = "malformed";
    CandidateProcessingStatus["ERROR"] = "error";
})(CandidateProcessingStatus || (CandidateProcessingStatus = {}));
// Candidate Download Status
export var CandidateDownloadStatus;
(function (CandidateDownloadStatus) {
    CandidateDownloadStatus["OK"] = "ok";
    CandidateDownloadStatus["MALFORMED"] = "malformed";
    CandidateDownloadStatus["NOT_FOUND"] = "notfound";
    CandidateDownloadStatus["ERROR"] = "error";
    CandidateDownloadStatus["NO_PERMISSION"] = "noperm";
    CandidateDownloadStatus["DELETED"] = "deleted";
    CandidateDownloadStatus["UNAPPLIED"] = "unapplied";
})(CandidateDownloadStatus || (CandidateDownloadStatus = {}));
// Debug Status
export var ImageStatus;
(function (ImageStatus) {
    ImageStatus["FOUND"] = "found";
    ImageStatus["UNUSED"] = "unused";
    ImageStatus["MISSING"] = "missing";
    ImageStatus["MALFORMED"] = "malformed";
    ImageStatus["FETCHING_FAILED"] = "fetching_failed";
    ImageStatus["TIMEOUT"] = "timeout";
    ImageStatus["OTHER"] = "other";
})(ImageStatus || (ImageStatus = {}));
//# sourceMappingURL=debugImage.jsx.map