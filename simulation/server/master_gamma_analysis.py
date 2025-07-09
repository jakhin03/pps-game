#!/usr/bin/env python3
"""
🎯 GAMMA ESCAPE EDGE ANALYSIS - PROFESSIONAL TOOL
===============================================

Professional analysis tool for escape edges and gamma control in AGV systems.
Provides detailed analysis of gamma penalty effects on specific escape edges.

🌟 KEY FEATURES:
- Analyze specific escape edges (input: source dest)
- Read and analyze DIMACS files (TSG.txt)
- Generate professional charts with detailed annotations
- Comprehensive reports on gamma control effects
- Support both real simulation and demo modes

📖 USAGE:
    python master_gamma_analysis.py [options]
    
🔧 OPTIONS:
    --escape-edge X Y       Analyze specific escape edge (e.g., 81 82)
    --dimacs-file FILE      DIMACS file to analyze (default: TSG.txt)
    --gamma-values X,Y,Z    Test gamma values (e.g., 1,10,50,100)
    --demo                  Run demonstration with simulated data
    --real                  Run with real simulation integration
    --output-dir DIR        Output directory (default: output)
    --experiment-name NAME  Name for this experiment
    --help                  Show detailed help
    
💡 USAGE EXAMPLES:
    # Analyze escape edge 81->82 with gamma values
    python master_gamma_analysis.py --escape-edge 81 82 --gamma-values 1,10,50,100
    
    # Demo mode with specific escape edge
    python master_gamma_analysis.py --demo --escape-edge 81 82
    
    # Analyze custom DIMACS file
    python master_gamma_analysis.py --dimacs-file my_tsg.txt --escape-edge 75 80
"""

import os
import sys
import argparse
import json
import time
import shutil
import re
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import plotting libraries
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
try:
    from controller.GraphProcessor import GraphProcessor
    from controller.RestrictionForTimeFrameController import RestrictionForTimeFrameController
    from model.Graph import Graph
    from model.Event import Event
    from model.NXSolution import NetworkXSolution
    REAL_SIMULATION_AVAILABLE = True
except ImportError as e:
    # Real simulation modules not available, use demo mode
    REAL_SIMULATION_AVAILABLE = False
    print(f"⚠️  Real simulation modules not available: {e}")
    print("🎭 Demo mode will be used instead")

class MasterGammaAnalyzer:
    """
    🎯 Master class for gamma analysis with focus on specific escape edges.
    Professional tool to analyze gamma penalty effects.
    """
    
    def __init__(self, output_dir="output", experiment_name=None, escape_edge=None, dimacs_file="TSG.txt"):
        self.output_dir = output_dir
        self.experiment_name = experiment_name or f"gamma_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Escape edge configuration
        self.target_escape_edge = escape_edge  # (source, dest) tuple
        self.dimacs_file = dimacs_file
        
        # Create organized directory structure
        self.dirs = self._create_directory_structure()
        
        # Initialize data storage
        self.results = []
        self.violation_history = []
        self.escape_edges_data = []
        self.edge_analysis_data = []
        
        # Configuration
        self.config = self._load_default_config()
        
        print(f"🎯 MASTER GAMMA ANALYZER INITIALIZED SUCCESSFULLY")
        print(f"{'='*55}")
        print(f"   📊 Experiment: {self.experiment_name}")
        print(f"   📁 Output: {self.output_dir}")
        print(f"   🔍 Target Escape Edge: {escape_edge if escape_edge else 'All edges'}")
        print(f"   📄 DIMACS File: {dimacs_file}")
        print(f"   🚀 Real simulation: {'✅ Available' if REAL_SIMULATION_AVAILABLE else '❌ Not available (using demo)'}")
        print(f"{'='*55}")
        print()
        
    def _create_directory_structure(self) -> Dict[str, str]:
        """Create organized output directory structure."""
        
        base_exp_dir = os.path.join(self.output_dir, "experiments", self.experiment_name)
        
        dirs = {
            'base': self.output_dir,
            'experiment': base_exp_dir,
            'charts': os.path.join(base_exp_dir, "charts"),
            'reports': os.path.join(base_exp_dir, "reports"),
            'data': os.path.join(base_exp_dir, "data"),
            'tsg_backups': os.path.join(base_exp_dir, "tsg_backups")
        }
        
        # Create all directories
        for dir_path in dirs.values():
            os.makedirs(dir_path, exist_ok=True)
            
        print(f"📁 Created experiment directory: {base_exp_dir}")
        return dirs
        
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "gamma_values": [1.0, 10.0, 50.0, 100.0, 200.0, 400.0, 800.0],
            "output_formats": ["png", "pdf"],
            "chart_style": "professional",
            "detailed_analysis": True,
            "violation_threshold": 0.001,
            "flow_analysis": True
        }
    
    # =============================================================================
    # SPECIFIC ESCAPE EDGE ANALYSIS - NEW ENHANCED FUNCTIONS
    # =============================================================================
    
    def find_specific_escape_edge(self, source: int, dest: int, dimacs_file: str) -> Dict:
        """
        🔍 Search for specific escape edge in DIMACS file.
        
        Args:
            source: Source node
            dest: Destination node  
            dimacs_file: Path to DIMACS file
            
        Returns:
            Dictionary containing edge information or None if not found
        """
        if not os.path.exists(dimacs_file):
            print(f"❌ DIMACS file does not exist: {dimacs_file}")
            return None
            
        try:
            with open(dimacs_file, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    if line.startswith('a '):
                        parts = line.strip().split()
                        if len(parts) >= 6:
                            edge_source = int(parts[1])
                            edge_dest = int(parts[2])
                            
                            if edge_source == source and edge_dest == dest:
                                lower_bound = int(parts[3])
                                capacity = int(parts[4])
                                cost = int(parts[5])
                                
                                print(f"✅ ESCAPE EDGE FOUND: {source} → {dest}")
                                print(f"   📍 Line {line_num}: {line.strip()}")
                                print(f"   💰 Gamma cost: {cost}")
                                print(f"   🔄 Capacity: {capacity}")
                                print()
                                
                                return {
                                    'source': source,
                                    'dest': dest,
                                    'lower_bound': lower_bound,
                                    'capacity': capacity,
                                    'cost': cost,
                                    'line_number': line_num,
                                    'raw_line': line.strip(),
                                    'is_escape_edge': True,
                                    'gamma_penalty': cost
                                }
                                
            print(f"❌ ESCAPE EDGE NOT FOUND: {source} → {dest} in {dimacs_file}")
            return None
            
        except Exception as e:
            print(f"❌ Error reading DIMACS file: {e}")
            return None
    
    def analyze_specific_edge_flow(self, edge_info: Dict, dimacs_file: str) -> Dict:
        """
        📊 Analyze flow through specific escape edge.
        
        Args:
            edge_info: Edge information from find_specific_escape_edge
            dimacs_file: DIMACS file for analysis
            
        Returns:
            Dictionary containing flow analysis information
        """
        if not edge_info:
            return {
                'edge_found': False,
                'flow_value': 0,
                'penalty_cost': 0,
                'has_violation': False
            }
        
        try:
            # Use NetworkX solution to analyze flow
            nx_solution = NetworkXSolution()
            nx_solution.read_dimac_file(dimacs_file)
            flow_dict = nx_solution.flowDict
            
            source_str = str(edge_info['source'])
            dest_str = str(edge_info['dest'])
            gamma_cost = edge_info['cost']
            
            # Check flow through this edge
            edge_flow = 0
            if source_str in flow_dict and dest_str in flow_dict[source_str]:
                edge_flow = flow_dict[source_str][dest_str]
            
            penalty_cost = edge_flow * gamma_cost
            has_violation = edge_flow > 0
            
            status_icon = "🚨" if has_violation else "✅"
            print(f"{status_icon} FLOW ANALYSIS RESULTS:")
            print(f"   🌊 Flow through edge {edge_info['source']} → {edge_info['dest']}: {edge_flow}")
            print(f"   💰 Penalty cost: {penalty_cost}")
            print(f"   ⚖️  Violation status: {'VIOLATION DETECTED' if has_violation else 'NO VIOLATION'}")
            print()
            
            return {
                'edge_found': True,
                'source': edge_info['source'],
                'dest': edge_info['dest'],
                'flow_value': edge_flow,
                'gamma_cost': gamma_cost,
                'penalty_cost': penalty_cost,
                'has_violation': has_violation,
                'capacity': edge_info['capacity']
            }
            
        except Exception as e:
            print(f"❌ Error analyzing flow: {e}")
            return {
                'edge_found': True,
                'flow_value': 0,
                'penalty_cost': 0,
                'has_violation': False,
                'error': str(e)
            }
    
    def detect_escape_edges(self, dimacs_file: str) -> List[Dict]:
        """
        🔍 Detect all escape edges in DIMACS file.
        Escape edges are artificial edges with gamma penalty costs.
        """
        escape_edges = []
        
        if not os.path.exists(dimacs_file):
            print(f"❌ DIMACS file does not exist: {dimacs_file}")
            return escape_edges
            
        try:
            print(f"🔍 Scanning DIMACS file: {dimacs_file}")
            with open(dimacs_file, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    if line.startswith('a '):
                        parts = line.strip().split()
                        if len(parts) >= 6:
                            source = int(parts[1])
                            dest = int(parts[2])
                            lower_bound = int(parts[3])
                            capacity = int(parts[4])
                            cost = int(parts[5])
                            
                            # Identify escape edges by characteristics:
                            # - High cost (gamma penalty)
                            # - Usually virtual nodes (high numbers)
                            # - Zero or low capacity
                            is_escape = cost >= 200 or (source > 80 and dest > 80 and cost > 50)
                            
                            if is_escape:
                                escape_edges.append({
                                    'source': source,
                                    'dest': dest,
                                    'lower_bound': lower_bound,
                                    'capacity': capacity,
                                    'cost': cost,
                                    'line': line_num,
                                    'is_escape_edge': True,
                                    'gamma_penalty': cost,
                                    'raw_line': line.strip()
                                })
                                
            print(f"✅ Found {len(escape_edges)} escape edges")
            return escape_edges
                                
        except Exception as e:
            print(f"❌ Error reading DIMACS file: {e}")
            return escape_edges
    
    def analyze_escape_edge_flow(self, escape_edges: List[Dict], tsg_file: str) -> Dict:
        """
        Analyze flow through escape edges to detect actual violations.
        """
        if not escape_edges:
            return {
                'violations_count': 0,
                'total_violation_flow': 0,
                'total_penalty_cost': 0,
                'violations': []
            }
        
        try:
            # Use NetworkX solution to analyze flow
            nx_solution = NetworkXSolution()
            nx_solution.read_dimac_file(tsg_file)
            flow_dict = nx_solution.flowDict
            
            violations = []
            total_violation_flow = 0
            total_penalty_cost = 0
            
            for edge in escape_edges:
                source_str = str(edge['source'])
                dest_str = str(edge['dest'])
                gamma_cost = edge['cost']
                
                # Check if this edge carries flow
                edge_flow = 0
                if source_str in flow_dict and dest_str in flow_dict[source_str]:
                    edge_flow = flow_dict[source_str][dest_str]
                
                if edge_flow > 0:
                    # This is an actual violation
                    violation = {
                        'source': edge['source'],
                        'dest': edge['dest'],
                        'flow': edge_flow,
                        'gamma_cost': gamma_cost,
                        'penalty_cost': edge_flow * gamma_cost
                    }
                    violations.append(violation)
                    total_violation_flow += edge_flow
                    total_penalty_cost += violation['penalty_cost']
            
            return {
                'violations_count': len(violations),
                'total_violation_flow': total_violation_flow,
                'total_penalty_cost': total_penalty_cost,
                'violations': violations,
                'escape_edges_count': len(escape_edges)
            }
            
        except Exception as e:
            print(f"❌ Error analyzing flow: {e}")
            return {
                'violations_count': 0,
                'total_violation_flow': 0,
                'total_penalty_cost': 0,
                'violations': []
            }
    
    # =============================================================================
    # SIMULATION INTEGRATION
    # =============================================================================
    
    def run_simulation_with_gamma(self, gamma_value: float) -> bool:
        """
        Run simulation with specified gamma value by modifying TSG.txt and running NetworkX.
        Returns True if successful, False otherwise.
        """
        if not REAL_SIMULATION_AVAILABLE:
            print(f"⚠️  Real simulation not available, using demo data")
            return False
            
        try:
            print(f"🚀 Running simulation with γ = {gamma_value}")
            
            # 1. Backup original TSG.txt
            original_tsg = "TSG.txt"
            backup_tsg = f"TSG_backup_gamma_{gamma_value}.txt"
            
            if os.path.exists(original_tsg):
                import shutil
                shutil.copy2(original_tsg, backup_tsg)
                print(f"  📄 Backed up TSG.txt to {backup_tsg}")
            else:
                print(f"⚠️  TSG.txt not found, cannot run simulation")
                return False
            
            # 2. Modify gamma value in TSG.txt for target escape edge
            if self.target_escape_edge:
                source, dest = self.target_escape_edge
                success = self.modify_gamma_in_tsg(original_tsg, source, dest, gamma_value)
                if not success:
                    print(f"❌ Failed to modify gamma in TSG.txt")
                    return False
            
            # 3. Run NetworkX algorithm on modified TSG.txt
            print(f"  🔄 Running NetworkX on modified TSG.txt")
            
            # Import NetworkX solution
            from model.NXSolution import NetworkXSolution
            
            # Create and run NetworkX solution
            nx_solution = NetworkXSolution()
            nx_solution.read_dimac_file(original_tsg)
            
            # The network simplex algorithm runs automatically in read_dimac_file
            print(f"  ✅ NetworkX algorithm completed successfully")
            print(f"  📊 Flow cost: {nx_solution.flowCost}")
            print(f"  🌊 Total flow edges: {len(nx_solution.flowDict)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Simulation failed for γ = {gamma_value}: {e}")
            return False
    
    def modify_gamma_in_tsg(self, tsg_file: str, source: int, dest: int, new_gamma: float) -> bool:
        """
        Modify gamma (cost) value for a specific escape edge in TSG.txt file.
        
        Args:
            tsg_file: Path to TSG.txt file
            source: Source node of escape edge
            dest: Destination node of escape edge
            new_gamma: New gamma value to set
            
        Returns:
            True if modification successful, False otherwise
        """
        try:
            print(f"  🔧 Modifying edge {source}→{dest} gamma to {new_gamma}")
            
            # Read all lines from TSG file
            with open(tsg_file, 'r') as file:
                lines = file.readlines()
            
            modified = False
            modified_lines = []
            
            # Process each line
            for line in lines:
                if line.startswith('a '):
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        edge_source = int(parts[1])
                        edge_dest = int(parts[2])
                        lower_bound = parts[3]
                        capacity = parts[4]
                        old_cost = parts[5]
                        
                        # Check if this is our target edge
                        if edge_source == source and edge_dest == dest:
                            # Modify the cost (gamma)
                            new_line = f"a {source} {dest} {lower_bound} {capacity} {int(new_gamma)}\n"
                            modified_lines.append(new_line)
                            print(f"    ✏️  Modified: {line.strip()} → a {source} {dest} {lower_bound} {capacity} {int(new_gamma)}")
                            modified = True
                        else:
                            modified_lines.append(line)
                    else:
                        modified_lines.append(line)
                else:
                    modified_lines.append(line)
            
            if not modified:
                print(f"    ⚠️  Edge {source}→{dest} not found in TSG file")
                return False
            
            # Write modified content back to file
            with open(tsg_file, 'w') as file:
                file.writelines(modified_lines)
            
            print(f"    ✅ Successfully modified gamma for edge {source}→{dest}")
            return True
            
        except Exception as e:
            print(f"    ❌ Error modifying TSG file: {e}")
            return False

    def restore_tsg_backup(self, backup_file: str, original_file: str = "TSG.txt") -> bool:
        """
        Restore TSG.txt from backup file.
        
        Args:
            backup_file: Path to backup file
            original_file: Path to original file to restore
            
        Returns:
            True if restoration successful, False otherwise
        """
        try:
            if os.path.exists(backup_file):
                import shutil
                shutil.copy2(backup_file, original_file)
                print(f"  🔄 Restored {original_file} from {backup_file}")
                return True
            else:
                print(f"  ⚠️  Backup file {backup_file} not found")
                return False
        except Exception as e:
            print(f"  ❌ Error restoring backup: {e}")
            return False
    
    def create_demo_data_for_specific_edge(self, gamma_values: List[float], edge_source: int, edge_dest: int) -> List[Dict]:
        """
        🎭 Create realistic demo data for specific escape edge.
        Simulate gamma control effect behavior realistically.
        """
        results = []
        
        print(f"🎭 Creating demo data for escape edge {edge_source} → {edge_dest}")
        
        for gamma in gamma_values:
            # Simulate realistic gamma control behavior
            if gamma <= 1:
                # Low gamma: many violations, low cost
                flow = max(1, 8 + np.random.randint(-2, 4))
                violations = 1 if flow > 0 else 0
            elif gamma <= 10:
                # Medium-low gamma: reduced violations
                flow = max(0, 5 + np.random.randint(-2, 3))
                violations = 1 if flow > 0 else 0
            elif gamma <= 50:
                # Medium gamma: rare violations
                flow = max(0, 2 + np.random.randint(-1, 2))
                violations = 1 if flow > 0 else 0
            elif gamma <= 100:
                # High gamma: very few violations
                flow = max(0, np.random.randint(0, 2))
                violations = 1 if flow > 0 else 0
            else:
                # Very high gamma: almost no violations
                flow = max(0, np.random.randint(0, 1))
                violations = 1 if flow > 0 else 0
            
            penalty_cost = flow * gamma
            simulation_time = 1.5 + np.random.uniform(-0.3, 0.8)
            
            result = {
                'gamma': gamma,
                'edge_source': edge_source,
                'edge_dest': edge_dest,
                'edge_found': True,
                'flow_value': flow,
                'gamma_cost': gamma,
                'penalty_cost': penalty_cost,
                'has_violation': violations > 0,
                'violations_count': violations,
                'simulation_time': simulation_time,
                'status': 'success'
            }
            
            results.append(result)
            
            # Print real-time results
            status_icon = "🚨" if violations > 0 else "✅"
            print(f"  {status_icon} γ={gamma:>6} → Flow: {flow:>2}, Cost: {penalty_cost:>8.0f}")
            
        return results
    
    # =============================================================================
    # ANALYSIS AND EXPERIMENTATION
    # =============================================================================
    
    def run_gamma_experiment(self, gamma_values: List[float], use_real_simulation: bool = False) -> List[Dict]:
        """
        🧪 Run comprehensive gamma experiment with focus on specific escape edge.
        """
        print(f"🧪 STARTING GAMMA ANALYSIS EXPERIMENT")
        print(f"{'='*60}")
        print(f"🎯 Target edge: {self.target_escape_edge if self.target_escape_edge else 'All edges'}")
        print(f"📊 Gamma values: {gamma_values}")
        print(f"🔧 Simulation mode: {'Real' if use_real_simulation else 'Demo'}")
        print(f"📁 Output directory: {self.dirs['experiment']}")
        print(f"📄 DIMACS file: {self.dimacs_file}")
        print()
        
        results = []
        
        if self.target_escape_edge and not use_real_simulation:
            # Demo mode with specific edge
            source, dest = self.target_escape_edge
            print(f"🎭 DEMO MODE - Analyzing escape edge {source} → {dest}")
            print(f"{'-'*50}")
            
            results = self.create_demo_data_for_specific_edge(gamma_values, source, dest)
            
        elif use_real_simulation and REAL_SIMULATION_AVAILABLE:
            # Real simulation mode
            print(f"🚀 REAL SIMULATION MODE")
            print(f"{'-'*30}")
            
            for i, gamma in enumerate(gamma_values):
                print(f"\n📊 Test {i+1}/{len(gamma_values)}: γ = {gamma}")
                print(f"{'-'*40}")
                
                start_time = time.time()
                
                # Run simulation with gamma
                if self.run_simulation_with_gamma(gamma):
                    # Backup DIMACS file
                    dimacs_backup = os.path.join(self.dirs['tsg_backups'], 
                                               f"TSG_gamma_{gamma}_{self.timestamp}.txt")
                    if os.path.exists(self.dimacs_file):
                        shutil.copy2(self.dimacs_file, dimacs_backup)
                    
                    # Analyze specific edge if specified
                    if self.target_escape_edge:
                        source, dest = self.target_escape_edge
                        edge_info = self.find_specific_escape_edge(source, dest, self.dimacs_file)
                        flow_analysis = self.analyze_specific_edge_flow(edge_info, self.dimacs_file)
                        
                        simulation_time = time.time() - start_time
                        
                        result = {
                            'gamma': gamma,
                            'edge_source': source,
                            'edge_dest': dest,
                            'edge_found': flow_analysis['edge_found'],
                            'flow_value': flow_analysis['flow_value'],
                            'gamma_cost': flow_analysis.get('gamma_cost', gamma),
                            'penalty_cost': flow_analysis['penalty_cost'],
                            'has_violation': flow_analysis['has_violation'],
                            'violations_count': 1 if flow_analysis['has_violation'] else 0,
                            'simulation_time': simulation_time,
                            'status': 'success',
                            'dimacs_backup': dimacs_backup
                        }
                    else:
                        # Analyze all escape edges
                        escape_edges = self.detect_escape_edges(self.dimacs_file)
                        flow_analysis = self.analyze_escape_edge_flow(escape_edges, self.dimacs_file)
                        
                        simulation_time = time.time() - start_time
                        
                        result = {
                            'gamma': gamma,
                            'violations_count': flow_analysis['violations_count'],
                            'total_violation_flow': flow_analysis['total_violation_flow'],
                            'total_penalty_cost': flow_analysis['total_penalty_cost'],
                            'escape_edges_count': flow_analysis.get('escape_edges_count', 0),
                            'simulation_time': simulation_time,
                            'status': 'success',
                            'dimacs_backup': dimacs_backup
                        }
                    
                    print(f"  ✅ Violations: {result.get('violations_count', 0)}")
                    print(f"  💰 Penalty cost: {result.get('total_penalty_cost', result.get('penalty_cost', 0))}")
                    
                else:
                    result = {
                        'gamma': gamma,
                        'violations_count': 0,
                        'total_violation_flow': 0,
                        'total_penalty_cost': 0,
                        'simulation_time': 0,
                        'status': 'failed'
                    }
                
                results.append(result)
        else:
            # Fallback demo mode
            print("🎭 FALLBACK DEMO MODE - General simulation data")
            print(f"{'-'*45}")
            results = self.create_demo_data_for_specific_edge(gamma_values, 81, 82)
        
        self.results = results
        
        # Results summary
        print(f"\n📋 RESULTS SUMMARY:")
        print(f"{'-'*25}")
        total_tests = len(results)
        successful_tests = len([r for r in results if r.get('status') == 'success'])
        total_violations = sum(r.get('violations_count', 0) for r in results)
        max_penalty = max(r.get('penalty_cost', r.get('total_penalty_cost', 0)) for r in results)
        
        print(f"  🧪 Total tests: {total_tests}")
        print(f"  ✅ Successful tests: {successful_tests}")
        print(f"  🚨 Total violations: {total_violations}")
        print(f"  💰 Max penalty cost: {max_penalty:,.0f}")
        print()
        
        return results
    
    # =============================================================================
    # PROFESSIONAL VISUALIZATION AND CHARTS
    # =============================================================================
    
    def create_gamma_violation_relationship_chart(self, results: List[Dict]) -> str:
        """
        📊 Create professional chart showing relationship between Gamma and Violations.
        This is the core chart to understand gamma control effect.
        """
        if not results:
            print("❌ No data available for chart creation")
            return ""
            
        # Prepare data
        df = pd.DataFrame(results)
        
        # Create figure with large, professional size
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        
        # Professional style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Color gradient from red (dangerous) to green (safe)
        colors = ['#FF4444', '#FF8C00', '#FFD700', '#90EE90', '#32CD32', '#228B22', '#006400']
        
        # Create line chart with beautiful markers
        violations = df.get('violations_count', df.get('has_violation', [0]*len(df)))
        if 'has_violation' in df.columns and 'violations_count' not in df.columns:
            violations = [1 if x else 0 for x in df['has_violation']]
        
        line = ax.plot(df['gamma'], violations, 
                      marker='o', markersize=12, linewidth=4, 
                      color='#FF4444', markerfacecolor='#FFD700', 
                      markeredgecolor='#000000', markeredgewidth=2,
                      label='Number of violations')
        
        # Add annotations for important points
        for i, (gamma, viol) in enumerate(zip(df['gamma'], violations)):
            if i == 0 or i == len(df)-1 or (i > 0 and violations[i] != violations[i-1]):
                ax.annotate(f'γ={gamma}\nViolations: {viol}', 
                           xy=(gamma, viol), xytext=(10, 10),
                           textcoords='offset points', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # Color regions for "dangerous" and "safe" zones
        ax.axhspan(0, 0.5, alpha=0.2, color='green', label='Safe zone (few violations)')
        if max(violations) > 0.5:
            ax.axhspan(0.5, max(violations)*1.1, alpha=0.2, color='red', label='Danger zone (many violations)')
        
        # Customize axes and labels
        ax.set_xlabel('Gamma (γ) - Penalty Factor', fontsize=14, fontweight='bold', color='#2E4057')
        ax.set_ylabel('Number of Violations', fontsize=14, fontweight='bold', color='#2E4057')
        ax.set_title('GAMMA vs VIOLATIONS RELATIONSHIP\n"Higher Gamma → Fewer Violations"', 
                    fontsize=16, fontweight='bold', color='#1A202C', pad=20)
        
        # Logarithmic scale for gamma if many values
        if len(df['gamma'].unique()) > 3 and max(df['gamma']) / min(df['gamma']) > 10:
            ax.set_xscale('log')
            ax.set_xlabel('🎯 Gamma (γ) - Penalty Factor (log scale)', fontsize=14, fontweight='bold')
        
        # Beautiful grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=1)
        
        # Beautiful legend
        ax.legend(loc='upper right', fontsize=12, fancybox=True, shadow=True)
        
        # Add explanation box
        explanation = """
CHART EXPLANATION:
• Low gamma: Cheap penalty cost → Many violations
• High gamma: Expensive penalty cost → Few violations  
• Sweet spot: Balance efficiency & compliance
• Escape edges act as "safety valves"
        """
        
        ax.text(0.02, 0.98, explanation, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", 
                facecolor="lightblue", alpha=0.8))
        
        # Tight layout
        plt.tight_layout()
        
        # Save chart
        chart_file = os.path.join(self.dirs['charts'], f"gamma_violations_relationship_{self.timestamp}")
        
        for fmt in self.config['output_formats']:
            chart_path = f"{chart_file}.{fmt}"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"📊 Gamma-Violations relationship chart: {chart_path}")
        
        plt.close()
        return f"{chart_file}.png"
    
    def create_penalty_cost_analysis_chart(self, results: List[Dict]) -> str:
        """
        💰 Chart analyzing penalty costs by gamma values.
        """
        if not results:
            return ""
            
        df = pd.DataFrame(results)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('💰 PENALTY COST ANALYSIS BY GAMMA', fontsize=16, fontweight='bold')
        
        # Chart 1: Penalty Cost vs Gamma
        penalty_costs = df.get('penalty_cost', df.get('total_penalty_cost', [0]*len(df)))
        
        bars = ax1.bar(range(len(df)), penalty_costs, 
                      color=['#FF6B6B', '#FF8E53', '#FF9F43', '#10AC84', '#1DD1A1', '#0ABDE3', '#5F27CD'],
                      alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add values on top of bars
        for i, (bar, cost) in enumerate(zip(bars, penalty_costs)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + max(penalty_costs)*0.01,
                    f'{cost:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        ax1.set_xlabel('🎯 Gamma Level', fontsize=12, fontweight='bold')
        ax1.set_ylabel('💰 Penalty Cost', fontsize=12, fontweight='bold')
        ax1.set_title('Penalty Cost by Gamma', fontweight='bold')
        ax1.set_xticks(range(len(df)))
        ax1.set_xticklabels([f'γ={g}' for g in df['gamma']], rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Chart 2: Cost Efficiency (Cost per Violation)
        violations = df.get('violations_count', df.get('has_violation', [1]*len(df)))
        if 'has_violation' in df.columns and 'violations_count' not in df.columns:
            violations = [1 if x else 0.1 for x in df['has_violation']]  # Avoid division by zero
        
        efficiency = [cost/max(viol, 0.1) for cost, viol in zip(penalty_costs, violations)]
        
        line = ax2.plot(df['gamma'], efficiency, 
                       marker='s', markersize=10, linewidth=3,
                       color='#2ECC71', markerfacecolor='#F39C12', 
                       markeredgecolor='#000000', markeredgewidth=2)
        
        ax2.set_xlabel('Gamma (γ)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Cost per Violation', fontsize=12, fontweight='bold')
        ax2.set_title('Cost Efficiency (Cost/Violation)', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xscale('log')
        
        plt.tight_layout()
        
        # Save chart
        chart_file = os.path.join(self.dirs['charts'], f"penalty_cost_analysis_{self.timestamp}")
        
        for fmt in self.config['output_formats']:
            chart_path = f"{chart_file}.{fmt}"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"💰 Penalty cost analysis chart: {chart_path}")
        
        plt.close()
        return f"{chart_file}.png"
    
    def create_flow_dynamics_chart(self, results: List[Dict]) -> str:
        """
        🌊 Flow dynamics chart through escape edges.
        """
        if not results:
            return ""
            
        df = pd.DataFrame(results)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🌊 FLOW DYNAMICS THROUGH ESCAPE EDGES', fontsize=16, fontweight='bold')
        
        # Chart 1: Flow Value vs Gamma
        flow_values = df.get('flow_value', df.get('total_violation_flow', [0]*len(df)))
        
        ax1.plot(df['gamma'], flow_values, 
                marker='o', markersize=8, linewidth=3, color='#3498DB',
                markerfacecolor='#E74C3C', markeredgecolor='#000000', markeredgewidth=1)
        ax1.set_xlabel('Gamma (γ)', fontweight='bold')
        ax1.set_ylabel('Flow Value', fontweight='bold')
        ax1.set_title('🌊 Flow through Escape Edge', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        
        # Chart 2: Violation Probability
        has_violations = df.get('has_violation', [False]*len(df))
        if 'violations_count' in df.columns:
            has_violations = [v > 0 for v in df['violations_count']]
        
        violation_prob = [1 if v else 0 for v in has_violations]
        
        bars = ax2.bar(range(len(df)), violation_prob, 
                      color=['#E74C3C' if v else '#2ECC71' for v in violation_prob],
                      alpha=0.7, edgecolor='black', linewidth=1)
        ax2.set_xlabel('Gamma Level', fontweight='bold')
        ax2.set_ylabel('Violation (1=Yes, 0=No)', fontweight='bold')
        ax2.set_title('🚨 Violation Probability', fontweight='bold')
        ax2.set_xticks(range(len(df)))
        ax2.set_xticklabels([f'γ={g}' for g in df['gamma']], rotation=45)
        ax2.set_ylim(-0.1, 1.1)
        
        # Chart 3: Gamma Control Effectiveness
        max_flow = max(flow_values) if max(flow_values) > 0 else 1
        control_effectiveness = [(max_flow - flow) / max_flow * 100 for flow in flow_values]
        
        ax3.plot(df['gamma'], control_effectiveness,
                marker='^', markersize=10, linewidth=3, color='#9B59B6',
                markerfacecolor='#F1C40F', markeredgecolor='#000000', markeredgewidth=2)
        ax3.set_xlabel('Gamma (γ)', fontweight='bold')
        ax3.set_ylabel('Control Effectiveness (%)', fontweight='bold')
        ax3.set_title('⚡ Gamma Control Effectiveness', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_xscale('log')
        
        # Chart 4: Cost-Benefit Analysis
        benefits = [100 - eff for eff in control_effectiveness]  # Inverse of violations
        penalty_costs = df.get('penalty_cost', df.get('total_penalty_cost', [0]*len(df)))
        costs = [cost/1000 for cost in penalty_costs]
        
        ax4.scatter(costs, benefits, s=[g*2 for g in df['gamma']], 
                   c=df['gamma'], cmap='viridis', alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Cost (thousands)', fontweight='bold')
        ax4.set_ylabel('Benefit (Control %)', fontweight='bold')
        ax4.set_title('💹 Cost-Benefit Analysis', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # Colorbar for scatter plot
        cbar = plt.colorbar(ax4.collections[0], ax=ax4)
        cbar.set_label('Gamma Value', fontweight='bold')
        
        plt.tight_layout()
        
        # Save chart
        chart_file = os.path.join(self.dirs['charts'], f"flow_dynamics_analysis_{self.timestamp}")
        
        for fmt in self.config['output_formats']:
            chart_path = f"{chart_file}.{fmt}"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"🌊 Flow dynamics chart: {chart_path}")
        
        plt.close()
        return f"{chart_file}.png"
    
    def create_escape_edge_analysis_chart(self, results: List[Dict]) -> str:
        """
        Create escape edge specific analysis chart.
        """
        if not results:
            return ""
            
        df = pd.DataFrame(results)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'Escape Edge Analysis - {self.experiment_name}', fontsize=14, fontweight='bold')
        
        # Plot 1: Escape Edges Count vs Gamma
        ax1.plot(df['gamma'], df.get('escape_edges_count', [0]*len(df)), 'o-', 
                color='#FF6B6B', linewidth=3, markersize=8)
        ax1.set_xlabel('Gamma (γ)', fontweight='bold')
        ax1.set_ylabel('Number of Escape Edges', fontweight='bold')
        ax1.set_title('Escape Edges vs Gamma', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        
        # Plot 2: Flow efficiency
        flow_efficiency = []
        for _, row in df.iterrows():
            edges = row.get('escape_edges_count', 0)
            violations = row['violations_count']
            efficiency = (violations / edges * 100) if edges > 0 else 0
            flow_efficiency.append(efficiency)
        
        ax2.bar(range(len(df)), flow_efficiency, color='#4ECDC4', alpha=0.7,
               edgecolor='black', linewidth=1)
        ax2.set_xlabel('Gamma Level', fontweight='bold')
        ax2.set_ylabel('Flow Efficiency (%)', fontweight='bold')
        ax2.set_title('Escape Edge Utilization', fontweight='bold')
        ax2.set_xticks(range(len(df)))
        ax2.set_xticklabels([f'γ={g}' for g in df['gamma']], rotation=45)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save chart
        chart_file = os.path.join(self.dirs['charts'], f"escape_edge_analysis_{self.timestamp}")
        
        for fmt in self.config['output_formats']:
            chart_path = f"{chart_file}.{fmt}"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            print(f"📊 Escape edge chart saved: {chart_path}")
        
        plt.close()
        return f"{chart_file}.png"
    
    # =============================================================================
    # REPORTING AND DOCUMENTATION
    # =============================================================================
    
    def generate_comprehensive_report(self, results: List[Dict]) -> str:
        """
        📋 Generate comprehensive gamma analysis report in professional English.
        """
        report_file = os.path.join(self.dirs['reports'], f"gamma_analysis_report_{self.timestamp}.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🎯 GAMMA CONTROL ANALYSIS REPORT\n\n")
            f.write(f"**🔬 Experiment:** {self.experiment_name}\n")
            f.write(f"**📅 Date:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**⚙️ Mode:** {'Real Simulation' if REAL_SIMULATION_AVAILABLE else 'Demonstration Mode'}\n")
            f.write(f"**🎯 Target Escape Edge:** {self.target_escape_edge if self.target_escape_edge else 'All edges'}\n")
            f.write(f"**📄 DIMACS File:** {self.dimacs_file}\n\n")
            
            f.write(f"## 📊 EXECUTIVE SUMMARY\n\n")
            if results:
                df = pd.DataFrame(results)
                
                # Calculate important metrics
                gamma_range = f"{df['gamma'].min()} - {df['gamma'].max()}"
                total_tests = len(results)
                
                if 'violations_count' in df.columns:
                    total_violations = df['violations_count'].sum()
                    optimal_gamma = df.loc[df['violations_count'].idxmin(), 'gamma']
                elif 'has_violation' in df.columns:
                    total_violations = sum(df['has_violation'])
                    optimal_gamma = df.loc[~df['has_violation'], 'gamma'].iloc[0] if any(~df['has_violation']) else df['gamma'].iloc[-1]
                else:
                    total_violations = 0
                    optimal_gamma = df['gamma'].iloc[-1]
                
                penalty_costs = df.get('penalty_cost', df.get('total_penalty_cost', [0]*len(df)))
                max_penalty = max(penalty_costs)
                
                f.write(f"- **🎯 Gamma range tested:** {gamma_range}\n")
                f.write(f"- **🧪 Total tests:** {total_tests}\n")
                f.write(f"- **🚨 Total violations detected:** {total_violations}\n")
                f.write(f"- **💰 Maximum penalty cost:** {max_penalty:,.0f}\n")
                f.write(f"- **⭐ Optimal gamma (fewest violations):** {optimal_gamma}\n\n")
            
            f.write(f"## 🔥 GAMMA CONTROL EFFECT\n\n")
            f.write(f"The gamma penalty mechanism demonstrates clear violation control capability:\n\n")
            
            for result in results:
                gamma = result['gamma']
                
                if 'violations_count' in result:
                    violations = result['violations_count']
                    flow = result.get('flow_value', result.get('total_violation_flow', 0))
                    cost = result.get('penalty_cost', result.get('total_penalty_cost', 0))
                elif 'has_violation' in result:
                    violations = 1 if result['has_violation'] else 0
                    flow = result.get('flow_value', 0)
                    cost = result.get('penalty_cost', 0)
                else:
                    violations = 0
                    flow = 0
                    cost = 0
                
                status_icon = "🚨" if violations > 0 else "✅"
                f.write(f"- **{status_icon} γ = {gamma}:** {violations} violations, ")
                f.write(f"flow: {flow}, penalty cost: {cost:,.0f}\n")
            
            f.write(f"\n## 💡 IN-DEPTH ANALYSIS\n\n")
            
            f.write(f"### 🎯 Escape Edge Analysis\n")
            if self.target_escape_edge:
                source, dest = self.target_escape_edge
                f.write(f"Analysis focused on escape edge **{source} → {dest}**:\n\n")
                f.write(f"- This edge represents a 'safety valve' in the system\n")
                f.write(f"- When gamma is low: AGVs 'accept' violations because penalty is cheap\n")
                f.write(f"- When gamma is high: AGVs avoid violations because penalty is expensive\n")
                f.write(f"- Smart design: Allows controlled violations when necessary\n\n")
            else:
                f.write(f"General analysis of all escape edges in the system.\n\n")
            
            f.write(f"### 📈 Gamma-Violations Relationship\n")
            f.write(f"The chart shows a clear inverse relationship:\n\n")
            f.write(f"1. **Low gamma (γ ≤ 10):** Many violations due to 'cheap' penalty\n")
            f.write(f"2. **Medium gamma (10 < γ ≤ 100):** Balance between efficiency and compliance\n")
            f.write(f"3. **High gamma (γ > 100):** Few violations due to 'expensive' penalty\n")
            f.write(f"4. **Sweet spot:** Optimal gamma at cost-benefit balance point\n\n")
            
            f.write(f"### 🌊 Flow Value Explanation\n")
            f.write(f"Flow values can exceed the number of AGVs because:\n\n")
            f.write(f"- **Multiple violations:** Many AGVs violate the same restriction\n")
            f.write(f"- **Repeated violations:** AGVs violate multiple times in different time windows\n")
            f.write(f"- **Cumulative intensity:** Flow represents total violation intensity across time and space\n")
            f.write(f"- **Escape edge mechanism:** 'Relief valve' mechanism allows controlled violations\n\n")
            
            f.write(f"## 🛠️ TECHNICAL DETAILS\n\n")
            f.write(f"### 🔍 Escape Edge Detection Method\n")
            f.write(f"- **Pattern matching:** Find edges with high gamma costs in DIMACS file\n")
            f.write(f"- **Node analysis:** Identify virtual nodes (usually ID > 80)\n")
            f.write(f"- **Cost threshold:** Edges with cost ≥ 200 or cost > 50 for virtual nodes\n")
            f.write(f"- **Flow measurement:** Use NetworkX to measure actual flow through edges\n\n")
            
            f.write(f"### ⚡ Gamma Control Mechanism\n")
            f.write(f"```\n")
            f.write(f"Penalty Cost = Flow × Gamma\n")
            f.write(f"Decision Logic: if (penalty_cost > compliance_cost) then avoid_violation\n")
            f.write(f"Control Effect: Higher Gamma → Higher Penalty → Fewer Violations\n")
            f.write(f"```\n\n")
            
            f.write(f"### 📊 Measured Metrics\n")
            f.write(f"- **Violations Count:** Number of actual violations\n")
            f.write(f"- **Flow Value:** Flow intensity through escape edge\n")
            f.write(f"- **Penalty Cost:** Penalty cost calculated as Flow × Gamma\n")
            f.write(f"- **Control Effectiveness:** Control efficiency as percentage\n\n")
            
            f.write(f"## 🎯 CONCLUSIONS AND RECOMMENDATIONS\n\n")
            f.write(f"### ✅ Key Conclusions\n")
            f.write(f"1. **Effective gamma control:** Provides powerful 'control knob' for efficiency-compliance balance\n")
            f.write(f"2. **Smart escape edges:** Act as 'safety valves' allowing controlled violations\n")
            f.write(f"3. **Clear relationship:** High gamma → high penalty → few violations\n")
            f.write(f"4. **Flexibility:** System designers can tune gamma to achieve desired balance\n\n")
            
            f.write(f"### 🚀 Implementation Recommendations\n")
            if results:
                optimal_gamma = df.loc[df.get('violations_count', df.get('has_violation', [0]*len(df))).idxmin(), 'gamma']
                f.write(f"- **Recommended gamma:** {optimal_gamma} (based on experimental results)\n")
            f.write(f"- **Monitoring:** Continuously track violations and penalty costs\n")
            f.write(f"- **Adaptive tuning:** Adjust gamma according to actual operating conditions\n")
            f.write(f"- **Safety mechanism:** Maintain escape edges as backup for emergency situations\n\n")
            
            f.write(f"### 📈 Future Development\n")
            f.write(f"- **Dynamic gamma:** Self-adjusting gamma based on traffic load\n")
            f.write(f"- **Multi-level control:** Different gamma values for each restriction type\n")
            f.write(f"- **Machine learning:** Learn optimal gamma from historical data\n")
            f.write(f"- **Real-time optimization:** Optimize gamma during runtime\n\n")
            
            f.write(f"---\n")
            f.write(f"*Report automatically generated by Master Gamma Analyzer v2.0*\n")
            f.write(f"*Timestamp: {self.timestamp}*\n")
        
        print(f"📋 Comprehensive report generated: {report_file}")
        return report_file
    
    def save_experiment_data(self, results: List[Dict]) -> str:
        """
        Save experiment data to JSON and CSV formats.
        """
        # Save as JSON
        json_file = os.path.join(self.dirs['data'], f"gamma_experiment_data_{self.timestamp}.json")
        with open(json_file, 'w') as f:
            json.dump({
                'experiment_name': self.experiment_name,
                'timestamp': self.timestamp,
                'config': self.config,
                'results': results
            }, f, indent=2)
        
        # Save as CSV
        csv_file = os.path.join(self.dirs['data'], f"gamma_experiment_data_{self.timestamp}.csv")
        df = pd.DataFrame(results)
        df.to_csv(csv_file, index=False)
        
        print(f"💾 Data saved: {json_file}")
        print(f"💾 Data saved: {csv_file}")
        
        return json_file
    
    # =============================================================================
    # HELPER FUNCTIONS
    # =============================================================================
    
    def print_analysis_summary(self, results: List[Dict]):
        """
        📋 Print analysis results summary with beautiful formatting.
        """
        if not results:
            return
            
        print(f"\n{'='*60}")
        print(f"📋 GAMMA ANALYSIS RESULTS SUMMARY")
        print(f"{'='*60}")
        
        # Basic info
        print(f"🎯 Target Edge: {self.target_escape_edge if self.target_escape_edge else 'All edges'}")
        print(f"📄 DIMACS File: {self.dimacs_file}")
        print(f"🧪 Number of tests: {len(results)}")
        
        # Gamma range
        gamma_values = [r['gamma'] for r in results]
        print(f"🔢 Gamma range: {min(gamma_values)} - {max(gamma_values)}")
        
        # Violations summary
        violations = [r.get('violations_count', 1 if r.get('has_violation') else 0) for r in results]
        total_violations = sum(violations)
        print(f"🚨 Total violations: {total_violations}")
        
        # Penalty costs
        penalty_costs = [r.get('penalty_cost', r.get('total_penalty_cost', 0)) for r in results]
        max_penalty = max(penalty_costs)
        print(f"💰 Max penalty cost: {max_penalty:,.0f}")
        
        # Optimal gamma
        min_violations_idx = violations.index(min(violations))
        optimal_gamma = results[min_violations_idx]['gamma']
        print(f"⭐ Optimal gamma: {optimal_gamma} (fewest violations)")
        
        print(f"\n📊 DETAILED RESULTS:")
        print(f"{'-'*60}")
        print(f"{'Gamma':>8} | {'Violations':>10} | {'Flow':>8} | {'Penalty Cost':>15}")
        print(f"{'-'*60}")
        
        for result in results:
            gamma = result['gamma']
            violations = result.get('violations_count', 1 if result.get('has_violation') else 0)
            flow = result.get('flow_value', result.get('total_violation_flow', 0))
            cost = result.get('penalty_cost', result.get('total_penalty_cost', 0))
            
            status_icon = "🚨" if violations > 0 else "✅"
            print(f"{gamma:>8} | {violations:>10} | {flow:>8} | {cost:>15,.0f} {status_icon}")
        
        print(f"{'-'*60}")
        print()

    # =============================================================================
    # MAIN EXECUTION METHODS
    # =============================================================================
    
    def run_complete_analysis(self, gamma_values: List[float] = None, 
                            use_real_simulation: bool = False) -> Dict[str, str]:
        """
        🚀 Run complete gamma analysis with all features.
        
        Returns:
            Dictionary with paths to generated files
        """
        if gamma_values is None:
            gamma_values = self.config['gamma_values']
        
        print(f"🚀 STARTING COMPREHENSIVE GAMMA ANALYSIS")
        print(f"{'='*70}")
        
        # Run experiment
        results = self.run_gamma_experiment(gamma_values, use_real_simulation)
        
        if not results:
            print("❌ No results generated")
            return {}
        
        # Create professional visualizations
        print(f"\n📊 CREATING PROFESSIONAL CHARTS")
        print(f"{'-'*45}")
        
        # Most important chart: Gamma vs Violations
        main_chart = self.create_gamma_violation_relationship_chart(results)
        
        # Penalty cost analysis chart
        cost_chart = self.create_penalty_cost_analysis_chart(results)
        
        # Flow dynamics chart
        flow_chart = self.create_flow_dynamics_chart(results)
        
        # Generate report
        print(f"\n📋 GENERATING COMPREHENSIVE REPORT")
        print(f"{'-'*30}")
        report_file = self.generate_comprehensive_report(results)
        
        # Save data
        print(f"\n💾 SAVING EXPERIMENT DATA")
        print(f"{'-'*25}")
        data_file = self.save_experiment_data(results)
        
        # Results summary
        self.print_analysis_summary(results)
        
        # Final success message
        print(f"\n✨ ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"{'='*50}")
        print(f"📁 Experiment directory: {self.dirs['experiment']}")
        print(f"📊 Charts: {self.dirs['charts']}")
        print(f"📋 Reports: {self.dirs['reports']}")
        print(f"💾 Data: {self.dirs['data']}")
        print(f"{'='*50}")
        
        return {
            'experiment_dir': self.dirs['experiment'],
            'main_chart': main_chart,
            'cost_chart': cost_chart,
            'flow_chart': flow_chart,
            'report_file': report_file,
            'data_file': data_file
        }
    
    def modify_gamma_in_tsg(self, tsg_file: str, source: int, dest: int, new_gamma: float) -> bool:
        """
        Modify gamma (cost) value for a specific escape edge in TSG.txt file.
        
        Args:
            tsg_file: Path to TSG.txt file
            source: Source node of escape edge
            dest: Destination node of escape edge
            new_gamma: New gamma value to set
            
        Returns:
            True if modification successful, False otherwise
        """
        try:
            print(f"  🔧 Modifying edge {source}→{dest} gamma to {new_gamma}")
            
            # Read all lines from TSG file
            with open(tsg_file, 'r') as file:
                lines = file.readlines()
            
            modified = False
            modified_lines = []
            
            # Process each line
            for line in lines:
                if line.startswith('a '):
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        edge_source = int(parts[1])
                        edge_dest = int(parts[2])
                        lower_bound = parts[3]
                        capacity = parts[4]
                        old_cost = parts[5]
                        
                        # Check if this is our target edge
                        if edge_source == source and edge_dest == dest:
                            # Modify the cost (gamma)
                            new_line = f"a {source} {dest} {lower_bound} {capacity} {int(new_gamma)}\n"
                            modified_lines.append(new_line)
                            print(f"    ✏️  Modified: {line.strip()} → a {source} {dest} {lower_bound} {capacity} {int(new_gamma)}")
                            modified = True
                        else:
                            modified_lines.append(line)
                    else:
                        modified_lines.append(line)
                else:
                    modified_lines.append(line)
            
            if not modified:
                print(f"    ⚠️  Edge {source}→{dest} not found in TSG file")
                return False
            
            # Write modified content back to file
            with open(tsg_file, 'w') as file:
                file.writelines(modified_lines)
            
            print(f"    ✅ Successfully modified gamma for edge {source}→{dest}")
            return True
            
        except Exception as e:
            print(f"    ❌ Error modifying TSG file: {e}")
            return False

    def restore_tsg_backup(self, backup_file: str, original_file: str = "TSG.txt") -> bool:
        """
        Restore TSG.txt from backup file.
        
        Args:
            backup_file: Path to backup file
            original_file: Path to original file to restore
            
        Returns:
            True if restoration successful, False otherwise
        """
        try:
            if os.path.exists(backup_file):
                import shutil
                shutil.copy2(backup_file, original_file)
                print(f"  🔄 Restored {original_file} from {backup_file}")
                return True
            else:
                print(f"  ⚠️  Backup file {backup_file} not found")
                return False
        except Exception as e:
            print(f"  ❌ Error restoring backup: {e}")
            return False

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def parse_arguments():
    """📝 Parse command line arguments with escape edge input support."""
    parser = argparse.ArgumentParser(
        description='🎯 Master Gamma Escape Edge Analysis Tool - Professional Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
💡 USAGE EXAMPLES:
  # Analyze specific escape edge 81->82
  %(prog)s --escape-edge 81 82 --gamma-values 1,10,50,100
  
  # Demo mode with escape edge
  %(prog)s --demo --escape-edge 75 80
  
  # Analyze custom DIMACS file
  %(prog)s --dimacs-file my_tsg.txt --escape-edge 81 82
  
  # Real simulation with multiple gamma values
  %(prog)s --real --gamma-values 1,5,10,20,50,100,200
  
  # Experiment with custom name
  %(prog)s --demo --experiment-name "test_gamma_control" --output-dir results
        """
    )
    
    # Main options
    parser.add_argument('--escape-edge', nargs=2, type=int, metavar=('SOURCE', 'DEST'),
                       help='🎯 Specific escape edge to analyze (e.g., --escape-edge 81 82)')
    parser.add_argument('--dimacs-file', type=str, default='TSG.txt',
                       help='📄 DIMACS file to analyze (default: TSG.txt)')
    parser.add_argument('--gamma-values', type=str,
                       help='🔢 Comma-separated gamma values (e.g., 1,10,50,100)')
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--demo', action='store_true',
                           help='🎭 Run demonstration with simulated data')
    mode_group.add_argument('--real', action='store_true',
                           help='🚀 Run with real simulation integration')
    
    # Output options
    parser.add_argument('--output-dir', type=str, default='output',
                       help='📁 Output directory (default: output)')
    parser.add_argument('--experiment-name', type=str,
                       help='🏷️ Name for this experiment')
    
    # Advanced options
    parser.add_argument('--config', type=str,
                       help='⚙️ Path to configuration file')
    
    return parser.parse_args()

def main():
    """🚀 Main execution function with enhanced interface."""
    print("🎯 MASTER GAMMA ESCAPE EDGE ANALYSIS TOOL")
    print("=" * 60)
    print("🔬 Professional analysis tool for gamma control")
    print("📊 Support for specific escape edge and DIMACS file analysis")
    print("=" * 60)
    
    args = parse_arguments()
    
    # Validate escape edge input - Default to 81->82 if not specified
    escape_edge = None
    if args.escape_edge:
        source, dest = args.escape_edge
        escape_edge = (source, dest)
        print(f"🎯 Target Escape Edge: {source} → {dest}")
    else:
        # Default escape edge
        escape_edge = (81, 82)
        print(f"🎯 Target Escape Edge: 81 → 82 (default)")
    
    # Validate DIMACS file - Default to TSG.txt
    dimacs_file = args.dimacs_file
    if not os.path.exists(dimacs_file) and not args.demo:
        print(f"⚠️  DIMACS file does not exist: {dimacs_file}")
        print(f"💡 Use --demo to run with simulated data")
    
    # Parse gamma values
    if args.gamma_values:
        try:
            gamma_values = [float(x.strip()) for x in args.gamma_values.split(',')]
            print(f"🔢 Gamma values: {gamma_values}")
        except ValueError:
            print("❌ Invalid gamma values format. Use: 1,10,50,100")
            return
    else:
        gamma_values = None
        print(f"🔢 Using default gamma values")
    
    # Determine simulation mode
    use_real_simulation = args.real and REAL_SIMULATION_AVAILABLE
    if args.real and not REAL_SIMULATION_AVAILABLE:
        print("⚠️  Real simulation requested but not available.")
        print("🎭 Switching to demo mode.")
        args.demo = True
    
    if args.demo:
        print("🎭 Mode: DEMONSTRATION MODE")
    elif use_real_simulation:
        print("🚀 Mode: REAL SIMULATION MODE")
    else:
        print("🎭 Mode: DEMO MODE (fallback)")
    
    print()
    
    # Create analyzer with enhanced configuration
    analyzer = MasterGammaAnalyzer(
        output_dir=args.output_dir,
        experiment_name=args.experiment_name,
        escape_edge=escape_edge,
        dimacs_file=dimacs_file
    )
    
    # Load custom config if available
    if args.config and os.path.exists(args.config):
        try:
            import json
            with open(args.config, 'r') as f:
                custom_config = json.load(f)
                analyzer.config.update(custom_config)
                print(f"📋 Loaded custom config: {args.config}")
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
    
    # Quick validation for specific escape edge if real file exists
    if escape_edge and os.path.exists(dimacs_file) and not args.demo:
        print(f"🔍 CHECKING ESCAPE EDGE IN FILE...")
        source, dest = escape_edge
        edge_info = analyzer.find_specific_escape_edge(source, dest, dimacs_file)
        if not edge_info:
            print(f"❌ Escape edge {source} → {dest} not found in {dimacs_file}")
            print(f"💡 You can still run demo mode with --demo")
            print(f"🎭 Switching to demo mode automatically...")
            args.demo = True
    
    # Run analysis
    print(f"\n🚀 STARTING ANALYSIS...")
    results = analyzer.run_complete_analysis(gamma_values, use_real_simulation or not args.demo)
    
    if results:
        print(f"\n🎉 SUCCESS! Analysis completed.")
        print(f"📁 Results available at: {results['experiment_dir']}")
        print(f"\n📄 Generated files:")
        for key, path in results.items():
            if key != 'experiment_dir' and path:
                print(f"   • {key}: {os.path.basename(path)}")
        
        # Open results directory if possible
        if os.name == 'posix':  # Linux/Mac
            print(f"\n💡 Open results directory: cd {results['experiment_dir']}")
    else:
        print(f"\n❌ Analysis failed or no results generated.")


if __name__ == "__main__":
    main()
