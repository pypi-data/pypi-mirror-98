import React from 'react';
import ScoreBar from 'app/components/scoreBar';
import Tooltip from 'app/components/tooltip';
import CHART_PALETTE from 'app/constants/chartPalette';
import { tct } from 'app/locale';
function UserMisery(props) {
    var bars = props.bars, barHeight = props.barHeight, miserableUsers = props.miserableUsers, miseryLimit = props.miseryLimit, totalUsers = props.totalUsers;
    var palette = new Array(bars).fill([CHART_PALETTE[0][0]]);
    var rawScore = Math.floor((miserableUsers / Math.max(totalUsers, 1)) * palette.length);
    var adjustedScore = rawScore > 0 ? rawScore : miserableUsers > 0 ? 1 : 0;
    var miseryPercentage = ((100 * miserableUsers) / Math.max(totalUsers, 1)).toFixed(2);
    var title = tct('[affectedUsers] out of [totalUsers] ([miseryPercentage]%) unique users waited more than [duration]ms', {
        affectedUsers: miserableUsers,
        totalUsers: totalUsers,
        miseryPercentage: miseryPercentage,
        duration: 4 * miseryLimit,
    });
    return (<Tooltip title={title} containerDisplayMode="block">
      <ScoreBar size={barHeight} score={adjustedScore} palette={palette} radius={0}/>
    </Tooltip>);
}
export default UserMisery;
//# sourceMappingURL=userMisery.jsx.map