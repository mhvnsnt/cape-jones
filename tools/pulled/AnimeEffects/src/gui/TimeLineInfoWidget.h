#ifndef GUI_INFOLABELWIDGET_H
#define GUI_INFOLABELWIDGET_H

#include <QLabel>
#include <QSettings>
#include "gui/GUIResources.h"
#include "gui/ViaPoint.h"
#include "core/Project.h"
#include "core/TimeInfo.h"
#include "core/TimeFormat.h"
#include "core/Animator.h"
#include "util/Range.h"
// Audio
#include "PlayBackWidget.h"
#include "AudioPlaybackWidget.h"

namespace gui {

class AudioWorker final: public QObject {
    Q_OBJECT
public:
    AudioWorker();
    ~AudioWorker();
    core::Project* mProject;
    PlayBackWidget* mPlayBack;
    int currentFrame;
    int latestFrame;
    int frameMax;
    int fps;

public slots:
    void onAudioUpdate();
    void setVars(core::Project* proj, PlayBackWidget* play,int cur, int last, int max, int frames);
    signals:
    void onAudioUpdated();
    void update();
};

class TimeLineInfoWidget: public QLabel {
public:
    TimeLineInfoWidget(GUIResources& aResources, QWidget* aParent);
    void setProject(core::Project* aProject);
    void setPlayback(PlayBackWidget* aPlayback);
    void onUpdate();

private:
    GUIResources& mResources;

    core::Project* mProject;
    PlayBackWidget* mPlayBack{};

    // IO OPS EVERY FRAME BAD //
    QSettings mSettings;
    core::TimeFormatType formatType = mSettings.value("generalsettings/ui/timeformat").isValid()
        ? static_cast<core::TimeFormatType>(mSettings.value("generalsettings/ui/timeformat").toInt())
        : core::TimeFormatType::TimeFormatType_Frames_From0;
    // --------------------- //
    int latestFrame = 0;
    bool mIsFirstTime;
    int mSuspendCount;
};

} // namespace gui


#endif // GUI_INFOLABELWIDGET_H
