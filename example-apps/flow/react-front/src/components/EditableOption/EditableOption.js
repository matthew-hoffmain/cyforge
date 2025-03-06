import React from "react";

export default function EditableOption({editing, name, value, setValue, options}) {
    const options_list = options.map((opt) => <option key={opt} name={name} value={opt}>{opt}</option>)


    return(
        editing ?
            <select name={name}
                    className="nodrag"
                    value={value}
                    onChange={e => setValue(e.target.value)}>>
                {options_list}
            </select> :
            value
    )
}