import {useState} from "react";

export default function EditableText({editing, name, value, setValue, ref}) {

    return(
        editing ?
            <input
                ref={ref}
                type="text"
                   className="nodrag"
                   name={name}
                   value={value}
                   onChange={e => setValue(e.target.value)}>
            </input> :
            value
    )
}