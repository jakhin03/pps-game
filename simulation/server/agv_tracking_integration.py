#!/usr/bin/env python3
"""
🚗 AGV Movement Tracking Integration
=====================================

This module extends the master_gamma_analysis.py to support AGV movement tracking
by integrating with the main simulation engine.

Key Features:
- 🔍 Real-time AGV position tracking
- 📊 Temporal analysis of AGV movements
- 🎯 Integration with gamma control analysis
- 📈 Movement pattern visualization
- 💾 AGV trajectory data export

Author: Enhanced Gamma Analysis System
Date: July 6, 2025
"""

import os
import sys
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Import simulation components
from model.AGV import AGV
from model.Graph import Graph
from model.Event import Event
from controller.GraphProcessor import GraphProcessor
from controller.EventGenerator import StartEvent
from discrevpy import simulator
from model.NXSolution import NetworkXSolution
import config

class AGVMovementTracker:
    """
    🚗 AGV Movement Tracker - Core tracking functionality
    """
    
    def __init__(self, output_dir: str = "agv_tracking_output"):
        self.output_dir = output_dir
        self.agv_positions = defaultdict(list)  # {agv_id: [(time, node_id), ...]}
        self.agv_paths = defaultdict(list)      # {agv_id: [node_id, ...]}
        self.movement_events = []               # [(time, agv_id, from_node, to_node), ...]
        self.time_snapshots = defaultdict(dict) # {time: {agv_id: node_id}}
        self.tracking_active = False
        self.start_time = None
        self.current_time = 0
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🚗 AGV Movement Tracker initialized")
        print(f"📁 Output directory: {output_dir}")
    
    def start_tracking(self):
        """Start AGV position tracking"""
        self.tracking_active = True
        self.start_time = time.time()
        self.current_time = 0
        print(f"🎬 AGV tracking started at {datetime.now()}")
    
    def stop_tracking(self):
        """Stop AGV position tracking"""
        self.tracking_active = False
        print(f"🛑 AGV tracking stopped at {datetime.now()}")
        self._save_tracking_data()
    
    def record_agv_position(self, agv_id: str, node_id: int, timestamp: float = None):
        """Record AGV position at given time"""
        if not self.tracking_active:
            return
            
        if timestamp is None:
            timestamp = time.time() - self.start_time
        
        self.agv_positions[agv_id].append((timestamp, node_id))
        self.time_snapshots[timestamp][agv_id] = node_id
        
        # Update current path
        if not self.agv_paths[agv_id] or self.agv_paths[agv_id][-1] != node_id:
            self.agv_paths[agv_id].append(node_id)
    
    def record_movement_event(self, agv_id: str, from_node: int, to_node: int, timestamp: float = None):
        """Record AGV movement event"""
        if not self.tracking_active:
            return
            
        if timestamp is None:
            timestamp = time.time() - self.start_time
        
        self.movement_events.append((timestamp, agv_id, from_node, to_node))
        print(f"🚗 AGV {agv_id}: {from_node} → {to_node} at t={timestamp:.2f}")
    
    def get_agv_position_at_time(self, agv_id: str, target_time: float) -> Optional[int]:
        """Get AGV position at specific time"""
        if agv_id not in self.agv_positions:
            return None
        
        positions = self.agv_positions[agv_id]
        if not positions:
            return None
        
        # Find the position at or before target_time
        for i in range(len(positions) - 1, -1, -1):
            timestamp, node_id = positions[i]
            if timestamp <= target_time:
                return node_id
        
        return positions[0][1]  # Return first position if target_time is before all records
    
    def get_all_agv_positions_at_time(self, target_time: float) -> Dict[str, int]:
        """Get all AGV positions at specific time"""
        positions = {}
        
        # Find the closest time snapshot
        closest_time = min(self.time_snapshots.keys(), 
                          key=lambda t: abs(t - target_time),
                          default=None)
        
        if closest_time is not None:
            positions.update(self.time_snapshots[closest_time])
        
        # Fill in missing AGVs
        for agv_id in self.agv_positions:
            if agv_id not in positions:
                pos = self.get_agv_position_at_time(agv_id, target_time)
                if pos is not None:
                    positions[agv_id] = pos
        
        return positions
    
    def get_agv_trajectory(self, agv_id: str) -> List[Tuple[float, int]]:
        """Get complete trajectory of an AGV"""
        return self.agv_positions.get(agv_id, [])
    
    def get_time_range(self) -> Tuple[float, float]:
        """Get the time range of tracked data"""
        all_times = []
        for positions in self.agv_positions.values():
            all_times.extend([t for t, _ in positions])
        
        if not all_times:
            return (0, 0)
        
        return (min(all_times), max(all_times))
    
    def _save_tracking_data(self):
        """Save tracking data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save AGV positions
        positions_file = os.path.join(self.output_dir, f"agv_positions_{timestamp}.json")
        with open(positions_file, 'w') as f:
            json.dump(dict(self.agv_positions), f, indent=2)
        
        # Save movement events
        events_file = os.path.join(self.output_dir, f"movement_events_{timestamp}.json")
        with open(events_file, 'w') as f:
            json.dump(self.movement_events, f, indent=2)
        
        # Save as CSV for analysis
        self._export_to_csv(timestamp)
        
        print(f"💾 Tracking data saved:")
        print(f"  📍 Positions: {positions_file}")
        print(f"  🔄 Events: {events_file}")
    
    def _export_to_csv(self, timestamp: str):
        """Export tracking data to CSV format"""
        # AGV positions CSV
        positions_data = []
        for agv_id, positions in self.agv_positions.items():
            for time_point, node_id in positions:
                positions_data.append({
                    'agv_id': agv_id,
                    'time': time_point,
                    'node_id': node_id
                })
        
        if positions_data:
            df_positions = pd.DataFrame(positions_data)
            positions_csv = os.path.join(self.output_dir, f"agv_positions_{timestamp}.csv")
            df_positions.to_csv(positions_csv, index=False)
            print(f"  📊 Positions CSV: {positions_csv}")
        
        # Movement events CSV
        if self.movement_events:
            events_data = []
            for time_point, agv_id, from_node, to_node in self.movement_events:
                events_data.append({
                    'time': time_point,
                    'agv_id': agv_id,
                    'from_node': from_node,
                    'to_node': to_node
                })
            
            df_events = pd.DataFrame(events_data)
            events_csv = os.path.join(self.output_dir, f"movement_events_{timestamp}.csv")
            df_events.to_csv(events_csv, index=False)
            print(f"  🔄 Events CSV: {events_csv}")


class AGVVisualizationEngine:
    """
    📊 AGV Movement Visualization Engine
    """
    
    def __init__(self, tracker: AGVMovementTracker):
        self.tracker = tracker
        self.output_dir = tracker.output_dir
    
    def create_agv_trajectory_chart(self, agv_ids: List[str] = None) -> str:
        """Create AGV trajectory visualization"""
        if agv_ids is None:
            agv_ids = list(self.tracker.agv_positions.keys())
        
        if not agv_ids:
            print("❌ No AGV data available for visualization")
            return ""
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set3
        
        for i, agv_id in enumerate(agv_ids):
            trajectory = self.tracker.get_agv_trajectory(agv_id)
            if not trajectory:
                continue
            
            times = [t for t, _ in trajectory]
            nodes = [n for _, n in trajectory]
            
            # Add trajectory line
            fig.add_trace(go.Scatter(
                x=times,
                y=nodes,
                mode='lines+markers',
                name=f'AGV {agv_id}',
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title='🚗 AGV Trajectories Over Time',
            xaxis_title='Time (seconds)',
            yaxis_title='Node ID',
            hovermode='x unified',
            showlegend=True,
            width=1200,
            height=800
        )
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_file = os.path.join(self.output_dir, f"agv_trajectories_{timestamp}.html")
        fig.write_html(chart_file)
        
        print(f"📊 AGV trajectory chart saved: {chart_file}")
        return chart_file
    
    def create_agv_heatmap(self, time_step: float = 1.0) -> str:
        """Create AGV position heatmap over time"""
        time_min, time_max = self.tracker.get_time_range()
        if time_min == time_max:
            print("❌ No time range data available")
            return ""
        
        # Generate time steps
        time_steps = np.arange(time_min, time_max + time_step, time_step)
        
        # Collect all node IDs
        all_nodes = set()
        for positions in self.tracker.agv_positions.values():
            all_nodes.update([n for _, n in positions])
        all_nodes = sorted(list(all_nodes))
        
        # Create heatmap data
        heatmap_data = []
        for t in time_steps:
            positions = self.tracker.get_all_agv_positions_at_time(t)
            node_counts = defaultdict(int)
            
            for agv_id, node_id in positions.items():
                node_counts[node_id] += 1
            
            row = [node_counts.get(node, 0) for node in all_nodes]
            heatmap_data.append(row)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=all_nodes,
            y=time_steps,
            colorscale='Viridis',
            colorbar=dict(title="Number of AGVs")
        ))
        
        fig.update_layout(
            title='🔥 AGV Position Heatmap Over Time',
            xaxis_title='Node ID',
            yaxis_title='Time (seconds)',
            width=1200,
            height=800
        )
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_file = os.path.join(self.output_dir, f"agv_heatmap_{timestamp}.html")
        fig.write_html(chart_file)
        
        print(f"🔥 AGV heatmap saved: {chart_file}")
        return chart_file
    
    def create_agv_animation(self, fps: int = 10) -> str:
        """Create animated AGV movement visualization"""
        time_min, time_max = self.tracker.get_time_range()
        if time_min == time_max:
            print("❌ No time range data available")
            return ""
        
        # Generate frames
        time_step = 1.0 / fps
        time_steps = np.arange(time_min, time_max + time_step, time_step)
        
        frames = []
        for t in time_steps:
            positions = self.tracker.get_all_agv_positions_at_time(t)
            
            frame_data = []
            for agv_id, node_id in positions.items():
                frame_data.append({
                    'agv_id': agv_id,
                    'node_id': node_id,
                    'x': node_id,  # Simplified positioning
                    'y': hash(agv_id) % 100,  # Simplified positioning
                    'time': t
                })
            
            frames.append(frame_data)
        
        # Create animation
        fig = go.Figure()
        
        # Add initial frame
        if frames:
            initial_frame = frames[0]
            fig.add_trace(go.Scatter(
                x=[d['x'] for d in initial_frame],
                y=[d['y'] for d in initial_frame],
                mode='markers+text',
                marker=dict(size=15, color='red'),
                text=[d['agv_id'] for d in initial_frame],
                textposition="middle center",
                name="AGVs"
            ))
        
        # Add animation frames
        animation_frames = []
        for i, frame_data in enumerate(frames):
            animation_frames.append(go.Frame(
                data=[go.Scatter(
                    x=[d['x'] for d in frame_data],
                    y=[d['y'] for d in frame_data],
                    mode='markers+text',
                    marker=dict(size=15, color='red'),
                    text=[d['agv_id'] for d in frame_data],
                    textposition="middle center"
                )],
                name=f"frame_{i}"
            ))
        
        fig.frames = animation_frames
        
        fig.update_layout(
            title='🎬 AGV Movement Animation',
            xaxis_title='Node Position',
            yaxis_title='AGV Layer',
            updatemenus=[{
                'type': 'buttons',
                'buttons': [
                    {'label': 'Play', 'method': 'animate', 'args': [None]},
                    {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]}
                ]
            }],
            width=1200,
            height=800
        )
        
        # Save animation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        animation_file = os.path.join(self.output_dir, f"agv_animation_{timestamp}.html")
        fig.write_html(animation_file)
        
        print(f"🎬 AGV animation saved: {animation_file}")
        return animation_file


class IntegratedGammaAGVAnalyzer:
    """
    🎯 Integrated Gamma Control + AGV Movement Analyzer
    Combines gamma analysis with AGV tracking for comprehensive analysis
    """
    
    def __init__(self, output_dir: str = "integrated_analysis"):
        self.output_dir = output_dir
        self.agv_tracker = AGVMovementTracker(os.path.join(output_dir, "agv_tracking"))
        self.visualization_engine = AGVVisualizationEngine(self.agv_tracker)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🎯 Integrated Gamma-AGV Analyzer initialized")
        print(f"📁 Output directory: {output_dir}")
    
    def run_integrated_simulation(self, gamma_values: List[float], 
                                 num_agvs: int = 5,
                                 simulation_duration: float = 100.0) -> Dict[str, Any]:
        """
        Run integrated simulation with gamma analysis and AGV tracking
        
        Args:
            gamma_values: List of gamma values to test
            num_agvs: Number of AGVs to simulate
            simulation_duration: Simulation duration in seconds
            
        Returns:
            Dictionary containing analysis results
        """
        print(f"🚀 STARTING INTEGRATED GAMMA-AGV SIMULATION")
        print(f"{'='*60}")
        print(f"📊 Gamma values: {gamma_values}")
        print(f"🚗 Number of AGVs: {num_agvs}")
        print(f"⏱️  Duration: {simulation_duration} seconds")
        print()
        
        results = {}
        
        for gamma in gamma_values:
            print(f"\n🧪 Testing gamma = {gamma}")
            print(f"{'-'*30}")
            
            # Start AGV tracking
            self.agv_tracker.start_tracking()
            
            # Run simulation with this gamma
            gamma_result = self._run_single_gamma_simulation(
                gamma, num_agvs, simulation_duration
            )
            
            # Stop AGV tracking
            self.agv_tracker.stop_tracking()
            
            # Analyze results
            agv_analysis = self._analyze_agv_movement(gamma)
            gamma_result['agv_analysis'] = agv_analysis
            
            results[gamma] = gamma_result
        
        # Create comprehensive analysis
        comprehensive_analysis = self._create_comprehensive_analysis(results)
        
        print(f"\n✅ INTEGRATED SIMULATION COMPLETED")
        print(f"📊 Results for {len(gamma_values)} gamma values")
        print(f"🚗 AGV movement data captured")
        print(f"📈 Comprehensive analysis generated")
        
        return comprehensive_analysis
    
    def _run_single_gamma_simulation(self, gamma: float, num_agvs: int, 
                                   duration: float) -> Dict[str, Any]:
        """Run simulation for single gamma value"""
        try:
            # Reset simulation state
            AGV.reset()
            simulator.reset()
            
            # Setup simulation
            graph_processor = GraphProcessor()
            graph_processor.use_in_main(False)
            
            # Create graph
            graph = Graph(graph_processor)
            
            # Create AGVs
            agvs = []
            for i in range(num_agvs):
                agv_id = f"AGV_{i+1}"
                start_node = i + 1  # Simple start node assignment
                agv = AGV(agv_id, start_node, graph)
                agvs.append(agv)
                
                # Record initial position
                self.agv_tracker.record_agv_position(agv_id, start_node, 0)
            
            # Setup events
            events = []
            for i, agv in enumerate(agvs):
                start_event = StartEvent(i, agv, graph)
                events.append(start_event)
            
            # Sort events by time
            events = sorted(events, key=lambda x: x.start_time)
            
            # Schedule events
            for event in events:
                simulator.schedule(event.start_time, event.process)
            
            # Run simulation
            simulator.ready()
            
            # Custom simulation loop with AGV tracking
            sim_start_time = time.time()
            current_sim_time = 0
            
            while current_sim_time < duration:
                # Step simulation
                simulator.step()
                current_sim_time = time.time() - sim_start_time
                
                # Record AGV positions
                for agv in agvs:
                    self.agv_tracker.record_agv_position(
                        agv.id, agv.current_node, current_sim_time
                    )
                
                # Check if simulation should continue
                if not simulator.has_events():
                    break
                
                # Small delay to prevent CPU overload
                time.sleep(0.01)
            
            # Analyze violations using NetworkX
            violations_analysis = self._analyze_violations(gamma)
            
            return {
                'gamma': gamma,
                'num_agvs': num_agvs,
                'duration': duration,
                'violations': violations_analysis,
                'agv_count': len(agvs),
                'simulation_time': current_sim_time,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"❌ Error in simulation: {e}")
            return {
                'gamma': gamma,
                'error': str(e),
                'status': 'failed'
            }
    
    def _analyze_violations(self, gamma: float) -> Dict[str, Any]:
        """Analyze violations using NetworkX"""
        try:
            # Check if TSG.txt exists
            if not os.path.exists("TSG.txt"):
                return {'violations_count': 0, 'note': 'No TSG.txt file found'}
            
            # Run NetworkX analysis
            nx_solution = NetworkXSolution()
            nx_solution.read_dimac_file("TSG.txt")
            
            # Count violations (simplified)
            violations = 0
            for source, flows in nx_solution.flowDict.items():
                for dest, flow in flows.items():
                    if flow > 0:
                        # Check if this is a violation edge
                        # (simplified check - in real implementation, 
                        # you'd check against escape edges)
                        if int(source) > 80 or int(dest) > 80:
                            violations += flow
            
            return {
                'violations_count': violations,
                'total_flow_cost': nx_solution.flowCost,
                'active_edges': len(nx_solution.flowDict)
            }
            
        except Exception as e:
            return {'violations_count': 0, 'error': str(e)}
    
    def _analyze_agv_movement(self, gamma: float) -> Dict[str, Any]:
        """Analyze AGV movement patterns"""
        analysis = {}
        
        # Basic statistics
        agv_count = len(self.agv_tracker.agv_positions)
        total_movements = len(self.agv_tracker.movement_events)
        time_range = self.agv_tracker.get_time_range()
        
        analysis['agv_count'] = agv_count
        analysis['total_movements'] = total_movements
        analysis['time_range'] = time_range
        analysis['duration'] = time_range[1] - time_range[0] if time_range[1] > time_range[0] else 0
        
        # Movement statistics per AGV
        agv_stats = {}
        for agv_id in self.agv_tracker.agv_positions:
            trajectory = self.agv_tracker.get_agv_trajectory(agv_id)
            unique_nodes = set([n for _, n in trajectory])
            
            agv_stats[agv_id] = {
                'total_positions': len(trajectory),
                'unique_nodes_visited': len(unique_nodes),
                'nodes_list': list(unique_nodes)
            }
        
        analysis['agv_statistics'] = agv_stats
        
        # Node utilization
        node_visits = defaultdict(int)
        for positions in self.agv_tracker.agv_positions.values():
            for _, node_id in positions:
                node_visits[node_id] += 1
        
        analysis['node_utilization'] = dict(node_visits)
        analysis['most_visited_nodes'] = sorted(node_visits.items(), 
                                              key=lambda x: x[1], reverse=True)[:5]
        
        return analysis
    
    def _create_comprehensive_analysis(self, results: Dict[float, Dict]) -> Dict[str, Any]:
        """Create comprehensive analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate visualizations
        print(f"\n📊 Generating visualizations...")
        trajectory_chart = self.visualization_engine.create_agv_trajectory_chart()
        heatmap_chart = self.visualization_engine.create_agv_heatmap()
        animation_file = self.visualization_engine.create_agv_animation()
        
        # Compile analysis
        analysis = {
            'timestamp': timestamp,
            'gamma_results': results,
            'summary': {
                'total_gamma_values': len(results),
                'successful_simulations': len([r for r in results.values() if r.get('status') == 'success']),
                'total_agvs_tracked': len(self.agv_tracker.agv_positions),
                'total_movements': len(self.agv_tracker.movement_events)
            },
            'visualizations': {
                'trajectory_chart': trajectory_chart,
                'heatmap_chart': heatmap_chart,
                'animation_file': animation_file
            }
        }
        
        # Save analysis
        analysis_file = os.path.join(self.output_dir, f"integrated_analysis_{timestamp}.json")
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        print(f"💾 Comprehensive analysis saved: {analysis_file}")
        
        return analysis


# Example usage and integration functions
def integrate_with_master_gamma_analysis():
    """
    Example of how to integrate AGV tracking with master_gamma_analysis.py
    """
    print(f"🔗 INTEGRATING AGV TRACKING WITH GAMMA ANALYSIS")
    print(f"{'='*55}")
    
    # Initialize integrated analyzer
    analyzer = IntegratedGammaAGVAnalyzer("integrated_gamma_agv_output")
    
    # Run integrated analysis
    gamma_values = [1.0, 10.0, 50.0, 100.0]
    results = analyzer.run_integrated_simulation(
        gamma_values=gamma_values,
        num_agvs=3,
        simulation_duration=30.0
    )
    
    print(f"\n✅ INTEGRATION COMPLETE")
    print(f"📊 Results: {len(results['gamma_results'])} gamma values analyzed")
    print(f"🚗 AGV tracking: {results['summary']['total_agvs_tracked']} AGVs tracked")
    print(f"🔄 Movements: {results['summary']['total_movements']} movements recorded")
    print(f"📈 Visualizations generated: {len(results['visualizations'])} files")
    
    return results


if __name__ == "__main__":
    # Run integrated analysis
    integrate_with_master_gamma_analysis()
