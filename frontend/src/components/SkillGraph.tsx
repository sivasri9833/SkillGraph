import {
  Background,
  Controls,
  Handle,
  MiniMap,
  Position,
  ReactFlow,
  type Edge,
  type Node,
  type NodeProps,
} from '@xyflow/react';
import { useCallback, useMemo, useState } from 'react';
import type { GraphData, GraphNode } from '../types';

interface FlowNodeData {
  label: string;
  nodeType: string;
  description?: string;
  difficulty?: string;
  category?: string;
}

const nodeStyles: Record<string, { bg: string; border: string; text: string }> = {
  career: { bg: '#eef2ff', border: '#6366f1', text: '#3730a3' },
  skill: { bg: '#ecfdf5', border: '#10b981', text: '#065f46' },
};

function CustomNode({ data, selected }: NodeProps) {
  const nodeData = data as unknown as FlowNodeData;
  const style = nodeStyles[nodeData.nodeType] ?? nodeStyles.skill;

  return (
    <div
      className={`rounded-lg border-2 px-4 py-2 shadow-sm transition-shadow ${
        selected ? 'shadow-md ring-2 ring-brand-300' : ''
      }`}
      style={{
        background: style.bg,
        borderColor: style.border,
        color: style.text,
        minWidth: 120,
      }}
    >
      <Handle type="target" position={Position.Top} className="!bg-slate-400" />
      <p className="text-xs font-medium uppercase opacity-60">{nodeData.nodeType}</p>
      <p className="text-sm font-semibold">{nodeData.label}</p>
      <Handle type="source" position={Position.Bottom} className="!bg-slate-400" />
    </div>
  );
}

const nodeTypes = { custom: CustomNode };

interface SkillGraphProps {
  graphData: GraphData;
  onNodeClick?: (node: GraphNode) => void;
}

function layoutNodes(graphNodes: GraphNode[]): Node[] {
  const career = graphNodes.find((n) => n.type === 'career');
  const skills = graphNodes.filter((n) => n.type === 'skill');

  const nodes: Node[] = [];

  if (career) {
    nodes.push({
      id: career.id,
      type: 'custom',
      position: { x: 300, y: 0 },
      data: { ...career, nodeType: 'career' } satisfies FlowNodeData,
    });
  }

  const cols = Math.ceil(Math.sqrt(skills.length)) || 1;
  skills.forEach((skill, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    nodes.push({
      id: skill.id,
      type: 'custom',
      position: { x: col * 180, y: 150 + row * 100 },
      data: { ...skill, nodeType: 'skill' } satisfies FlowNodeData,
    });
  });

  return nodes;
}

export default function SkillGraph({ graphData, onNodeClick }: SkillGraphProps) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);

  const nodes = useMemo(() => layoutNodes(graphData.nodes), [graphData.nodes]);

  const edges: Edge[] = useMemo(
    () =>
      graphData.edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.label.replace(/_/g, ' '),
        animated: e.label === 'REQUIRES',
        style: {
          stroke: e.label === 'REQUIRES' ? '#6366f1' : '#94a3b8',
          strokeWidth: e.label === 'REQUIRES' ? 2 : 1,
        },
        labelStyle: { fontSize: 10, fill: '#64748b' },
      })),
    [graphData.edges],
  );

  const onNodeClickHandler = useCallback(
    (_: React.MouseEvent, node: Node) => {
      const graphNode = graphData.nodes.find((n) => n.id === node.id);
      if (graphNode) {
        setSelectedNode(graphNode);
        onNodeClick?.(graphNode);
      }
    },
    [graphData.nodes, onNodeClick],
  );

  return (
    <div className="space-y-4">
      <div className="h-[420px] overflow-hidden rounded-xl border border-slate-200 bg-white">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={onNodeClickHandler}
          fitView
          fitViewOptions={{ padding: 0.3 }}
          proOptions={{ hideAttribution: true }}
        >
          <Background gap={16} color="#e2e8f0" />
          <Controls />
          <MiniMap
            nodeColor={(n) =>
              n.data?.nodeType === 'career' ? '#6366f1' : '#10b981'
            }
            maskColor="rgba(240, 240, 240, 0.8)"
          />
        </ReactFlow>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600">
        <span className="font-medium text-slate-700">Legend:</span>
        <span className="flex items-center gap-1.5">
          <span className="h-3 w-3 rounded border-2 border-brand-500 bg-brand-50" />
          Career
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-3 w-3 rounded border-2 border-emerald-500 bg-emerald-50" />
          Skill
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-0.5 w-6 bg-brand-500" />
          REQUIRES
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-0.5 w-6 bg-slate-400" />
          Prerequisite / Related
        </span>
      </div>

      {/* Selected node detail panel */}
      {selectedNode && (
        <div className="rounded-xl border border-slate-200 bg-white p-4">
          <div className="flex items-start justify-between">
            <div>
              <span
                className={`inline-block rounded px-2 py-0.5 text-xs font-medium uppercase ${
                  selectedNode.type === 'career'
                    ? 'bg-brand-100 text-brand-700'
                    : 'bg-emerald-100 text-emerald-700'
                }`}
              >
                {selectedNode.type}
              </span>
              <h4 className="mt-1 text-lg font-semibold text-slate-900">
                {selectedNode.label}
              </h4>
            </div>
            {selectedNode.difficulty && (
              <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600">
                {selectedNode.difficulty}
              </span>
            )}
          </div>
          {selectedNode.description && (
            <p className="mt-2 text-sm text-slate-600">{selectedNode.description}</p>
          )}
          {selectedNode.category && (
            <p className="mt-1 text-xs text-slate-400">Category: {selectedNode.category}</p>
          )}
        </div>
      )}
    </div>
  );
}
