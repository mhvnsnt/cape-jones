#ifndef UTIL_IDSOLVER
#define UTIL_IDSOLVER

#include <functional>
#include <QMap>
#include <QDebug>

namespace util {

template<typename tData>
class IDSolver {
public:
    typedef int IdType;
    typedef std::function<void(tData)> Solver;
    typedef std::pair<IdType, Solver> Referencer;

    IDSolver(): mDataMap(), mReferencers() {}

    void pushData(IdType aId, tData aData) { mDataMap[aId] = aData; }

    void pushReferencer(IdType aId, const Solver& aSolver) { mReferencers.push_back(Referencer(aId, aSolver)); }

    // we guarantee to call each solver by pushing order.
    QSettings settings;
    //bool FORCE_SOLVER_LOAD = settings.value("forceSolverLoad", false).toBool();
    // TODO: FIX THIS, this shit happens because we erase every cache
    bool FORCE_SOLVER_LOAD = true;
    bool solve() {
        for (auto refer : mReferencers) {
            if (!mDataMap.contains(refer.first)) {
                qDebug() << "Failed to solve id reference at "  << std::to_string(refer.first).c_str();
                if (!FORCE_SOLVER_LOAD) {
                    return false;
                }
            }
            refer.second(mDataMap[refer.first]);
        }
        return true;
    }

private:
    QMap<IdType, tData> mDataMap;
    QVector<Referencer> mReferencers;
};

} // namespace util

#endif // UTIL_IDSOLVER
