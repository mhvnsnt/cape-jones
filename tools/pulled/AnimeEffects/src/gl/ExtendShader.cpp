#include "gl/ExtendShader.h"
#include <QFile>
#include <QTextStream>
#include "XC.h"
#include "util/NetworkUtil.h"
#include <QDir>

#include <QRegularExpression>

namespace gl {

ExtendShader::ExtendShader():
    mOriginalCodeVert(), mOriginalCodeFrag(), mVertexCode(), mFragmentCode(), mVariation(), mLog() {}

bool ExtendShader::openFromFile(const QString& aFilePath, QString& originalCode) {
    mVariation.clear();
    QFile file(aFilePath);
    if (file.open(QIODevice::ReadOnly)) {
        QTextStream in(&file);
        originalCode = in.readAll();
        return true;
    }
    mLog = file.errorString() + "\n" + aFilePath;
    return false;
}

bool ExtendShader::openFromFileVert(const QString& aFilePath) { return openFromFile(aFilePath, mOriginalCodeVert); }

bool ExtendShader::openFromFileFrag(const QString& aFilePath) { return openFromFile(aFilePath, mOriginalCodeFrag); }

void ExtendShader::openFromText(const QString& aText, QString& originalCode) {
    mVariation.clear();
    originalCode = aText;
    mLog = "";
}

void ExtendShader::openFromTextVert(const QString& aText) { openFromText(aText, mOriginalCodeVert); }

void ExtendShader::openFromTextFrag(const QString& aText) { openFromText(aText, mOriginalCodeFrag); }

void ExtendShader::setVariationValue(const QString& aName, const QString& aValue) {
    VariationUnit unit = {aName, aValue};
    mVariation.push_back(unit);
}

bool ExtendShader::resolveVariation() {
    QTextStream out(&mVertexCode);
    mVertexCode.clear();

    QTextStream vertexIn(&mOriginalCodeVert);
    QTextStream fragmentIn(&mOriginalCodeFrag);

    mLog = "";
    bool isSuccess = true;

    int currentShader = 0; // 0 = vertex, 1 = fragment
    while (true) {
        QString line;
        if (currentShader == 0) {
            line = vertexIn.readLine();
            if (line.isNull()) {
                currentShader = 1;
                out.setString(&mFragmentCode);
                continue;
            }
        }
        if (currentShader == 1) {
            line = fragmentIn.readLine();
            if (line.isNull())
                break;
        }

        QRegularExpression lineReg("^#variation\\s+(.*)$");
        if (lineReg.match(line).hasMatch()) {
            QString nameValue = lineReg.match(line).captured(1);
            // XC_REPORT() << "nameValue" << nameValue;
            QRegularExpression nameReg("^(\\S+)");
            if (nameReg.match(nameValue).lastCapturedIndex() != -1) {
                QString name = nameReg.match(nameValue).captured(1);
                // XC_REPORT() << "name" << name;

                bool find = false;
                for (auto itr = mVariation.begin(); itr != mVariation.end(); ++itr) {
                    if (name == itr->name) {
                        line = "#define " + itr->name + " " + itr->value;
                        find = true;
                        break;
                    }
                }
                if (!find) {
                    line = "#define " + nameValue;
                }
            } else {
                mLog += "Invalid variation format:" + line + "\n";
                isSuccess = false;
            }
        }
        out << line << "\n";
    }

    return isSuccess;
}

} // namespace gl
