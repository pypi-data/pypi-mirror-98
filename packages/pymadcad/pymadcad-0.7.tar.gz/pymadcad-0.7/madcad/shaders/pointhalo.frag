#version 330

in vec2 uv;
uniform vec3 color;
uniform sampler2D halotex;

// render color
out vec4 out_color;

void main() {
	out_color = vec4(color, texture(halotex, uv).r);
}
