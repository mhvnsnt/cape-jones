#include "TimeFormat.h"

namespace core {

TimeFormat::TimeFormat(util::Range aRange, int aFps) {
    mRange = aRange;
    mFps = aFps;
}

QString TimeFormat::frameToString(const int aFrame, const TimeFormatType aTimeFormatType) const {
    switch (aTimeFormatType) {
    case TimeFormatType_Frames_From1:
        return QString::number(aFrame + 1);

    case TimeFormatType_Relative_FPS: {
        QString number = QString("%1").arg(aFrame / mFps, 0);
        return number;
    }

    case TimeFormatType_Seconds_Frames: { // (SS:FF)
        double min = 0.0;
        double max = 60.0;

        double nMin = 0;
        double nMax = 1;

        double seconds = util::MathUtil::remap(aFrame, min, max, nMin, nMax);

        QString n = QString("%1:%2")
                        .arg(static_cast<int>(seconds))
                        .arg(static_cast<int>(util::MathUtil::cycle(aFrame, 0.0, 60.0)), 2, 10, QLatin1Char('0'));

        return n;
    }

    case TimeFormatType_Timecode_SMPTE: { // (HH:MM:SS:FF)
        double min = 0.0;
        double max = 60.0;

        double nMin = 0;
        double nMax = 1000.0;

        double ms = util::MathUtil::remap(aFrame, min, max, nMin, nMax);

        DDHHMMSSmmm timeStruct = msToDDHHMMSSmmm(ms);

        QString n = QString("%1:%2:%3:%4")
                        .arg(timeStruct.hours)
                        .arg(timeStruct.minutes)
                        .arg(timeStruct.seconds)
                        .arg(static_cast<int>(util::MathUtil::cycle(aFrame, 0.0, 60.0)));

        return n;
    }

    case TimeFormatType_Timecode_HHMMSSmmm: { // (HH:MM:SS:mmm)
        double min = 0.0;
        double max = 60.0;

        double nMin = 0;
        double nMax = 1000.0;

        double ms = util::MathUtil::remap(aFrame, min, max, nMin, nMax);

        DDHHMMSSmmm timeStruct = msToDDHHMMSSmmm(ms);

        QString n = QString("%1:%2:%3:%4")
                        .arg(timeStruct.hours)
                        .arg(timeStruct.minutes)
                        .arg(timeStruct.seconds)
                        .arg(timeStruct.milliseconds);

        return n;
    }

    default:
        return QString::number(aFrame);
    }
}


DDHHMMSSmmm TimeFormat::msToDDHHMMSSmmm(double ms) {
    int d = 0, h = 0, m = 0, s = 0, mi = 0;
    // Days to milli
    if (ms >= 86400 * 1000) {
        d = qFloor(ms / 1000 / 60 / 60 / 24);
        ms = ms - d * (86400 * 1000);
    }
    // Hour to milli
    if (ms >= 3600 * 1000) {
        h = qFloor(ms / 1000 / 60 / 60);
        ms = ms - h * (3600 * 1000);
    }
    // Minute to milli
    if (ms >= 60 * 1000) {
        mi = qFloor(ms / 1000 / 60);
        ms = ms - mi * (60 * 1000);
    }
    // Second to milli
    if (ms >= 1000) {
        s = qFloor(ms / 1000);
        ms = ms - s * 1000;
    }
    DDHHMMSSmmm timeStruct;
    timeStruct.days = d;
    timeStruct.hours = h;
    timeStruct.minutes = m;
    timeStruct.seconds = s;
    timeStruct.milliseconds = static_cast<int>(ms);

    return timeStruct;
}

} // namespace core
