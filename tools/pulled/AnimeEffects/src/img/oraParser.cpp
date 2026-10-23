//
// Created by yukusai on 02/07/2025.
//

#include "oraParser.h"

#include "XCAssert.h"

#include <QFileInfo>

bool oraParser::charIsEqualTo(const char* cStr, const std::string& str) { return std::string(cStr) == str; }

QPixmap oraParser::createPattern(const QSize& size, const QColor& background, const QColor& foreground) {
    QPixmap pixmap(size);
    pixmap.fill(background);
    {
        QPainter painter(&pixmap);
        painter.setPen(foreground);
        painter.drawLine(0, size.height() / 2, size.width(), size.height() / 2);
        painter.drawLine(size.width() / 2, 0, size.width() / 2, size.height());
    }
    return pixmap;
}

void oraParser::parse(layerStack* layer_stack, pugi::xml_node::iterator::pointer xml_node) {
    bool visAttrExists = false;

    if(charIsEqualTo(xml_node->name(), "layer")){
        layer_stack->type = IMAGE;
        oraImage.oraImage.layerNumber += 1;
    }
    else if(charIsEqualTo(xml_node->name(), "stack")){
        layer_stack->type = FOLDER;
    }
    else{
        layer_stack->type = UNKNOWN;
        qDebug() << "Unknown stack sibling value: " << xml_node->name();
    }

    if (layer_stack->type == UNKNOWN) { return; }
    for(auto attr: xml_node->attributes()){
        if(charIsEqualTo(attr.name(), "src")){
            QImage img;
            try {
                img = QImage::fromData(QByteArray::fromStdString(oraFile->read(attr.as_string())))
                          .convertedTo(QImage::Format_RGBA8888);
            }
            catch(...){
                qDebug() << "Unable to read image at " << attr.as_string() << ". Utilizing fallback.";
                img = createPattern(QSize(1028, 1028)).toImage();
            }
            layer_stack->image = img;
        }
        else if(charIsEqualTo(attr.name(), "name")){
            layer_stack->name = attr.as_string();
            if(layer_stack->name.empty()) { layer_stack->name = "Unknown"; }
        }
        else if(charIsEqualTo(attr.name(), "x")){
            layer_stack->x = attr.as_int();
        }
        else if(charIsEqualTo(attr.name(), "y")){
            layer_stack->y = attr.as_int();
        }
        else if(charIsEqualTo(attr.name(), "opacity")){
            layer_stack->opacity = attr.as_float();
        }
        else if(charIsEqualTo(attr.name(), "visibility")){
            visAttrExists = true;
            layer_stack->isVisible = charIsEqualTo(attr.as_string(), "visible");
        }
        else if(charIsEqualTo(attr.name(), "composite-op")){
            layer_stack->composite = stringToComposite(attr.as_string());
        }
        else{
            qDebug() << "Unknown attribute: " << attr.name() << "; with value: " << attr.value();
        }
    }
    if(!visAttrExists){
        layer_stack->isVisible = true;
    }
    if (layer_stack->type == IMAGE) {
        layer_stack->rect = QRect(layer_stack->x, layer_stack->y, layer_stack->image.width(), layer_stack->image.height());
    }
    else {
        layer_stack->rect = QRect(layer_stack->x, layer_stack->y, 0, 0);
    }
    int capacity = 0;
    for ([[maybe_unused]] auto child: xml_node->children()) {
        capacity += 1;
    }
    layer_stack->capacity = capacity;
    oraImage.layers.append(*layer_stack);

    layerStack childLayer;
    for (auto sib: xml_node->next_sibling()) {
        parse(&childLayer, &sib);
    }

    for(auto child: xml_node->children()){
        parse(&childLayer, &child);
    }
}

bool oraParser::initialize() {
    const std::string stackStr = oraFile->read("stack.xml");
    XC_ASSERT(reader);
    const pugi::xml_parse_result result = reader->load_string(stackStr.c_str());
    if(result.status == pugi::xml_parse_status::status_ok){
        // Parse image
        const pugi::xml_node& Image = reader->child("image");
        oraImage.oraImage.width = Image.attribute("w").as_int();
        oraImage.oraImage.height = Image.attribute("h").as_int();
        oraImage.oraImage.oraVersion = Image.attribute("version").as_string();
        oraImage.oraImage.rect = QRect(0, 0, oraImage.oraImage.width, oraImage.oraImage.height);
        if(oraImage.oraImage.oraVersion.empty()){ oraImage.oraImage.oraVersion = "0.0.1"; }
        // Parse stacks
        pugi::xml_node mainStack = reader->child("image").child("stack");
        layerStack layer;
        layer.name = QFileInfo(QString::fromStdString(oraFile->get_filename())).baseName().toStdString();
        layer.type = ROOT;
        oraImage.layers.append(layer);
        layerStack childLayer;
        for (auto sib: mainStack.next_sibling()) {
            if(charIsEqualTo(sib.name(), "layer")){
                childLayer.type = IMAGE;
            }
            else if(charIsEqualTo(sib.name(), "stack")){
                childLayer.type = FOLDER;
            }
            else{
                qDebug() << "Unknown stack child type: " << sib.value();
            }
            parse(&childLayer, &sib);
        }

        for(auto child: mainStack.children()){
            if(charIsEqualTo(child.name(), "layer")){
                childLayer.type = IMAGE;
            }
            else if(charIsEqualTo(child.name(), "stack")){
                childLayer.type = FOLDER;
            }
            else{
                qDebug() << "Unknown stack child type: " << child.name();
            }
            parse(&childLayer, &child);
        }
    }
    else{
        qDebug() << result.status;
        delete reader;
        return false;
    }
    delete reader;
    return true;
}

