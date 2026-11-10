#ifndef GUI_MAINVIEWSETTING
#define GUI_MAINVIEWSETTING

namespace gui {

class MainViewSetting {
public:
    MainViewSetting(): showLayerMesh(), cutImagesByTheFrame(), rotateViewACW(), resetRotateView(), rotateViewCW(), flipCanvas() {}

    bool showLayerMesh;
    bool cutImagesByTheFrame;
    bool rotateViewACW;
    bool resetRotateView;
    bool rotateViewCW;
    bool flipCanvas;
};

} // namespace gui

#endif // GUI_MAINVIEWSETTING
