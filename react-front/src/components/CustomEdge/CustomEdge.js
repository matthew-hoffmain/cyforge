import React, {useEffect, useState} from 'react';
import {
    BaseEdge,
    EdgeLabelRenderer,
    getBezierPath, getSimpleBezierPath, getSmoothStepPath, getStraightPath,
    useReactFlow,
} from 'reactflow';

export default function CustomEdge({
                                       id,
                                       sourceX,
                                       sourceY,
                                       targetX,
                                       targetY,
                                       sourcePosition,
                                       targetPosition,
                                       style = {},
                                       data,
                                       markerEnd,
                                   }) {
    const { setEdges } = useReactFlow();
    const [dependent, setDependent] = useState(data.dependent);
    const centerX = sourceX;

    const [smoothEdgePath, smoothLabelX, smoothLabelY] = getSmoothStepPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    const [bezierEdgePath, bezierLabelX, bezierLabelY] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    function toggleEdge(edge) {
        setDependent(!dependent);
        edge.data.dependent = !dependent;
        edge.animated = !edge.animated;
        return edge;
    };

    const onEdgeClickToggle = () => {
        setEdges((edges) => edges.map(
            (edge) => edge.id === id ?
        toggleEdge(edge) :
        edge));
    };

    const onEdgeClickDelete = () => {
        setEdges((edges) => edges.filter((edge) => edge.id !== id));
    };


    return (
        <>
            <BaseEdge path={dependent ? bezierEdgePath : smoothEdgePath} markerEnd={markerEnd} style={style} />
             <EdgeLabelRenderer>
                <div
                    style={{
                        position: 'absolute',
                        transform: `translate(-50%, -50%) translate(${smoothLabelX}px,${smoothLabelY}px)`,
                        fontSize: 12,
                        // everything inside EdgeLabelRenderer has no pointer events by default
                        // if you have an interactive element, set pointer-events: all
                        pointerEvents: 'all',
                    }}
                    className="nodrag nopan"
                >
                    <button className="edgebutton" onClick={onEdgeClickToggle}>
                        Toggle
                    </button>

                </div>
            </EdgeLabelRenderer>
        </>
    );
}
