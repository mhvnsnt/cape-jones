#version 330

uniform bool setColor;

uniform float hue;
uniform float saturation;
uniform float value;

uniform vec4 uColor;
uniform sampler2D uTexture;

uniform sampler2D uDestTexture;

#variation IS_CLIPPEE 0

#if IS_CLIPPEE
uniform int uClippingId;
uniform usampler2D uClippingTexture;
#endif

in vec2 vTexCoord;
in vec2 vDestCoord;

layout(location = 0, index = 0) out vec4 oFragColor;


vec3 RGBtoHSV(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}


vec3 HSVtoRGB(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}


vec3 lowerBrightness(vec3 color, float brightness)
{
    brightness = 1.0 / brightness;
    color.x = pow(color.x, brightness);
    color.y = pow(color.y, brightness);
    color.z = pow(color.z, brightness);
    return color;
}


vec3 adjustBrightness(vec3 color, float brightness)
{
    float alpha = sign(brightness - 1.0) * 0.5 + 0.5;
    return mix(
        lowerBrightness(color, brightness),
        1.0 - lowerBrightness(1.0 - color, 2.0 - brightness),
        alpha
    );
}


float saturate(float x)
{
    return clamp(x, 0.0, 1.0);
}


vec3 offsetHSV(vec3 color)
{
    vec3 newColor = color;
    newColor = RGBtoHSV(newColor);
    if (setColor){
        newColor.x = hue;
    } else {
        newColor.x += hue;
    }
	newColor.x = fract(newColor.x);
    newColor.y = min(1.0, newColor.y * saturation);
    newColor.z = min(1.0, newColor.z * value);
    newColor = HSVtoRGB(newColor);
    return newColor;
}

void main(void)
{
    vec4 color = uColor * texture(uTexture, vTexCoord);
    color.xyz = offsetHSV(color.xyz);
    oFragColor = color;
	
    ivec2 destCoord = ivec2(vDestCoord);
    vec4 destColor = texelFetch(uDestTexture, destCoord, 0);
	
#if IS_CLIPPEE
    uvec2 clippingData = texelFetch(uClippingTexture, destCoord, 0).xy;
    if (uClippingId == int(clippingData.x))
    {
        color.a *= float(clippingData.y) / 255.0;
		oFragColor = destColor;
    }
    else
    {
        //oFragColor = destColor;
        discard;
    }
#endif
}
