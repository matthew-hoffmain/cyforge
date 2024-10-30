import styled from "styled-components";

function get_color(data) {
    const this_alpha = data.connected ? "FF" : "AA"

    return data.color + this_alpha;
}

function get_glow(data) {
    if (data.connected) {
        return "0 0 20px " + get_color(data);
    }
    else {
        return ''
    }
}

export function add_style(node) {
    return ({...node, data : {...node.data, style : styled.div`
            font-size: 12px;
            background: ${get_color({...node.data, id: node.id})};
            border: 2px solid #444;
            border-radius: 5px;
            text-align: left;
            padding: 5px;
            box-shadow: ${get_glow({...node.data, id: node.id})};
        .react-flow__handle {
            width: 7px;
            height: 7px;
            border-radius: 10px;
        }
    `
            }});
}