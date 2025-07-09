# 🎯 MASTER GAMMA ANALYSIS - WORKFLOW DOCUMENTATION

## 📋 Tổng quan

`master_gamma_analysis.py` là một công cụ phân tích chuyên nghiệp để nghiên cứu tác động của gamma control trong hệ thống AGV. Tool này hỗ trợ hai chế độ hoạt động chính:

- **🎭 Demo Mode**: Sử dụng dữ liệu mô phỏng để demo tính năng
- **🚀 Real Mode**: Phân tích trực tiếp trên file TSG.txt có sẵn với NetworkX

## 🆕 THAY ĐỔI MỚI TRONG PHIÊN BẢN 2.0

### ✨ Real Mode Mới
- **Input mặc định**: TSG.txt (file có sẵn) và escape edge 81→82
- **Luồng hoạt động**: Đọc TSG.txt → Sửa gamma → Chạy NetworkX → Phân tích kết quả
- **Không cần user input**: Hoàn toàn tự động, không cần nhập tham số simulation
- **Modification trực tiếp**: Thay đổi cost trong file TSG.txt thay vì tạo TSG mới

### 🎯 Default Configuration
- **DIMACS File**: `TSG.txt` (mặc định)
- **Target Escape Edge**: `81 → 82` (mặc định)
- **Gamma Values**: `[1.0, 10.0, 50.0, 100.0, 200.0, 400.0, 800.0]` (mặc định)
- **Analysis Method**: NetworkX network simplex algorithm

### 🔧 Simplified Workflow
1. **Backup** TSG.txt gốc
2. **Modify** gamma value trong TSG.txt cho escape edge target
3. **Execute** NetworkX algorithm trên file đã modify
4. **Analyze** flow qua escape edge để detect violations
5. **Repeat** cho mỗi gamma value

---

## 🔧 Kiến trúc hệ thống

### Core Components

```
master_gamma_analysis.py
├── MasterGammaAnalyzer (Main Class)
├── Command Line Interface
├── Visualization Engine
├── Report Generator
└── Data Exporter
```

### Dependencies

```
controller/
├── GraphProcessor
├── RestrictionForTimeFrameController
└── SimulationEngine

model/
├── Graph
├── Event
└── NXSolution

gamma_analysis/
└── integrated_gamma_control.py
```

---

## 🎭 DEMO MODE WORKFLOW

### 1. Khởi tạo hệ thống

```
🎯 MASTER GAMMA ANALYZER INITIALIZED
├── Output directory: output/experiments/gamma_analysis_YYYYMMDD_HHMMSS
├── Target escape edge: Tùy chọn (81→82 mặc định)
├── Gamma values: [1.0, 10.0, 50.0, 100.0, 200.0, 400.0, 800.0]
└── Mode: DEMONSTRATION
```

### 2. Tạo dữ liệu mô phỏng

```python
def create_demo_data_for_specific_edge():
    """
    Tạo dữ liệu mô phỏng thực tế cho escape edge
    """
    for gamma in gamma_values:
        if gamma <= 1:
            # Gamma thấp: Vi phạm nhiều, chi phí thấp
            flow = max(1, 8 + random(-2, 4))
            violations = 1 if flow > 0 else 0
        elif gamma <= 10:
            # Gamma trung bình thấp: Vi phạm giảm
            flow = max(0, 5 + random(-2, 3))
            violations = 1 if flow > 0 else 0
        elif gamma <= 50:
            # Gamma trung bình: Vi phạm hiếm
            flow = max(0, 2 + random(-1, 2))
            violations = 1 if flow > 0 else 0
        else:
            # Gamma cao: Gần như không vi phạm
            flow = max(0, random(0, 1))
            violations = 1 if flow > 0 else 0
        
        penalty_cost = flow * gamma
        return result_data
```

### 3. Luồng xử lý Demo

```
🎭 DEMO MODE EXECUTION
├── Parse command line arguments
├── Initialize MasterGammaAnalyzer
├── Create demo data for specific edge
├── Generate simulation results
├── Create professional charts
├── Generate comprehensive report
└── Save experiment data
```

### 4. Kết quả Demo

```
Demo Results Example:
γ=1.0   → Flow: 7, Cost: 7      🚨 VIOLATION
γ=10.0  → Flow: 7, Cost: 70     🚨 VIOLATION
γ=50.0  → Flow: 1, Cost: 50     🚨 VIOLATION
γ=100.0 → Flow: 1, Cost: 100    🚨 VIOLATION
γ=200.0 → Flow: 0, Cost: 0      ✅ NO VIOLATION
γ=400.0 → Flow: 0, Cost: 0      ✅ NO VIOLATION
γ=800.0 → Flow: 0, Cost: 0      ✅ NO VIOLATION
```

---

## 🚀 REAL MODE WORKFLOW

### 1. Khởi tạo Real Simulation

```
🚀 REAL SIMULATION MODE INITIALIZATION
├── Check TSG.txt file availability (mặc định)
├── Validate escape edge configuration (mặc định: 81→82)
├── Import NetworkX solution module
└── Initialize gamma control integration
```

### 2. Simulation Loop for Each Gamma

```python
def run_simulation_with_gamma(gamma_value):
    """
    Chạy simulation với gamma value cụ thể bằng cách:
    1. Backup TSG.txt
    2. Modify gamma trong TSG.txt
    3. Chạy NetworkX algorithm
    """
    # 1. Backup original TSG.txt
    original_tsg = "TSG.txt"
    backup_tsg = f"TSG_backup_gamma_{gamma_value}.txt"
    shutil.copy2(original_tsg, backup_tsg)
    
    # 2. Modify gamma value in TSG.txt for target escape edge
    success = modify_gamma_in_tsg(original_tsg, source, dest, gamma_value)
    
    # 3. Run NetworkX algorithm on modified TSG.txt
    nx_solution = NetworkXSolution()
    nx_solution.read_dimac_file(original_tsg)
    
    return simulation_success
```

### 3. Chi tiết Real Mode Execution

```
🚀 REAL MODE EXECUTION FLOW

Input Parameters (Mặc định):
├── DIMACS File: TSG.txt (có sẵn)
├── Target Escape Edge: 81 → 82 (mặc định)
└── Gamma Values: [1.0, 10.0, 50.0, 100.0, 200.0, 400.0, 800.0]

For each gamma_value in gamma_values:
    
    📊 Test X/Y: γ = {gamma_value}
    ├── � Backup TSG.txt → TSG_backup_gamma_{gamma_value}.txt
    ├── 🔧 Modify edge 81→82 gamma:
    │   ├── Read TSG.txt line by line
    │   ├── Find line: "a 81 82 0 1 [old_gamma]"
    │   ├── Replace with: "a 81 82 0 1 {gamma_value}"
    │   └── Write back to TSG.txt
    │
    ├── 🔄 Run NetworkX Algorithm:
    │   ├── nx_solution = NetworkXSolution()
    │   ├── nx_solution.read_dimac_file("TSG.txt")
    │   ├── Execute network simplex algorithm
    │   └── Calculate flow cost and flow dict
    │
    ├── 📊 Analyze results:
    │   ├── Find specific escape edge in modified TSG
    │   ├── Check flow through escape edge (81→82)
    │   ├── Calculate penalty costs (flow × gamma)
    │   └── Detect violations (flow > 0)
    │
    └── 💾 Backup modified TSG for analysis
```

### 4. Escape Edge Analysis

```python
def modify_gamma_in_tsg(tsg_file, source, dest, new_gamma):
    """
    Sửa đổi gamma (cost) cho escape edge cụ thể trong TSG.txt
    """
    # Read all lines from TSG file
    with open(tsg_file, 'r') as file:
        lines = file.readlines()
    
    # Find and modify target edge
    for line in lines:
        if line.startswith('a '):
            parts = line.strip().split()
            if int(parts[1]) == source and int(parts[2]) == dest:
                # Modify: "a 81 82 0 1 200" → "a 81 82 0 1 {new_gamma}"
                new_line = f"a {source} {dest} {parts[3]} {parts[4]} {int(new_gamma)}\n"
                # Replace line in file
                break
    
    # Write modified content back
    with open(tsg_file, 'w') as file:
        file.writelines(modified_lines)
```

### 5. Real Mode Results

```
Real Mode Results Example:
📊 Test 1/2: γ = 1.0
├── 📄 Backed up TSG.txt to TSG_backup_gamma_1.0.txt
├── 🔧 Modified: a 81 82 0 1 200 → a 81 82 0 1 1
├── 🔄 NetworkX algorithm completed successfully
├── 📊 Flow cost: 11, Total flow edges: 7
├── ✅ ESCAPE EDGE FOUND: 81 → 82 (gamma: 1)
├── 🌊 Flow through edge 81 → 82: 0
└── ⚖️ Violation status: NO VIOLATION

📊 Test 2/2: γ = 10.0
├── 📄 Backed up TSG.txt to TSG_backup_gamma_10.0.txt
├── 🔧 Modified: a 81 82 0 1 1 → a 81 82 0 1 10
├── 🔄 NetworkX algorithm completed successfully
├── 📊 Flow cost: 11, Total flow edges: 7
├── ✅ ESCAPE EDGE FOUND: 81 → 82 (gamma: 10)
├── 🌊 Flow through edge 81 → 82: 0
└── ⚖️ Violation status: NO VIOLATION
```

---

## 📊 VISUALIZATION & REPORTING

### 1. Professional Charts Generation

```
📊 CHARTS CREATION PIPELINE
├── create_gamma_violation_relationship_chart()
│   ├── Gamma vs Violations relationship
│   ├── Professional styling with seaborn
│   ├── Color coding (Red=Dangerous, Green=Safe)
│   └── Annotations for key points
│
├── create_penalty_cost_analysis_chart()
│   ├── Penalty Cost vs Gamma
│   ├── Cost Efficiency analysis
│   └── Bar charts with value labels
│
├── create_flow_dynamics_chart()
│   ├── Flow Value vs Gamma
│   ├── Violation Probability
│   ├── Control Effectiveness
│   └── Cost-Benefit Analysis
│
└── create_escape_edge_analysis_chart()
    ├── Escape Edges Count vs Gamma
    └── Flow efficiency metrics
```

### 2. Comprehensive Report Generation

```
📋 REPORT STRUCTURE
├── Executive Summary
│   ├── Gamma range tested
│   ├── Total violations detected
│   ├── Maximum penalty cost
│   └── Optimal gamma recommendation
│
├── Gamma Control Effect Analysis
│   ├── Low gamma behavior
│   ├── Medium gamma behavior
│   ├── High gamma behavior
│   └── Sweet spot identification
│
├── Technical Details
│   ├── Escape edge detection method
│   ├── Gamma control mechanism
│   ├── Measured metrics
│   └── Flow value explanation
│
└── Conclusions & Recommendations
    ├── Key findings
    ├── Implementation recommendations
    ├── Future development suggestions
    └── Performance optimization tips
```

---

## 🔍 ESCAPE EDGE DETECTION

### 1. DIMACS File Analysis

```python
def detect_escape_edges(dimacs_file):
    """
    Phát hiện escape edges trong file DIMACS
    """
    escape_edges = []
    
    with open(dimacs_file, 'r') as file:
        for line_num, line in enumerate(file, 1):
            if line.startswith('a '):
                parts = line.strip().split()
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
                        'cost': cost,
                        'capacity': capacity,
                        'is_escape_edge': True
                    })
    
    return escape_edges
```

### 2. Flow Analysis

```python
def analyze_escape_edge_flow(escape_edges, tsg_file):
    """
    Phân tích flow qua escape edges để phát hiện violations
    """
    nx_solution = NetworkXSolution()
    nx_solution.read_dimac_file(tsg_file)
    flow_dict = nx_solution.flowDict
    
    violations = []
    for edge in escape_edges:
        edge_flow = flow_dict.get(str(edge['source']), {}).get(str(edge['dest']), 0)
        
        if edge_flow > 0:
            # Đây là violation thực tế
            violation = {
                'source': edge['source'],
                'dest': edge['dest'],
                'flow': edge_flow,
                'gamma_cost': edge['cost'],
                'penalty_cost': edge_flow * edge['cost']
            }
            violations.append(violation)
    
    return violations
```

---

## 🎯 GAMMA CONTROL MECHANISM

### 1. Gamma Control Theory

```
💡 GAMMA CONTROL EXPLAINED:

Penalty Cost = Flow × Gamma
Decision Logic: if (penalty_cost > compliance_cost) then avoid_violation
Control Effect: Higher Gamma → Higher Penalty → Fewer Violations

🎯 Gamma Ranges:
├── γ ≤ 10:    "Cheap violations" → Many violations
├── 10 < γ ≤ 100: "Balanced" → Moderate violations  
├── γ > 100:   "Expensive violations" → Few violations
└── γ > 1000:  "Prohibitive" → Almost no violations
```

### 2. Implementation Details

```python
class RestrictionForTimeFrameController:
    def set_gamma_value(self, gamma_value: float):
        """
        Set gamma value for penalty cost calculation
        """
        self._min_gamma = gamma_value
        
        # Update gamma integrator
        if self.gamma_integrator:
            self.gamma_integrator.set_gamma_value(gamma_value)
        
        # Update existing restrictions
        for i, restriction in enumerate(self.restrictions):
            time_frames, restricted_edges, U, priority, _, k_val = restriction
            updated_restriction = (time_frames, restricted_edges, U, priority, gamma_value, k_val)
            self.restrictions[i] = updated_restriction
```

---

## 📁 OUTPUT STRUCTURE

### 1. Directory Organization

```
output/experiments/gamma_analysis_YYYYMMDD_HHMMSS/
├── charts/
│   ├── gamma_violations_relationship_YYYYMMDD_HHMMSS.png
│   ├── gamma_violations_relationship_YYYYMMDD_HHMMSS.pdf
│   ├── penalty_cost_analysis_YYYYMMDD_HHMMSS.png
│   ├── penalty_cost_analysis_YYYYMMDD_HHMMSS.pdf
│   ├── flow_dynamics_analysis_YYYYMMDD_HHMMSS.png
│   └── flow_dynamics_analysis_YYYYMMDD_HHMMSS.pdf
├── reports/
│   └── gamma_analysis_report_YYYYMMDD_HHMMSS.md
├── data/
│   ├── gamma_experiment_data_YYYYMMDD_HHMMSS.json
│   └── gamma_experiment_data_YYYYMMDD_HHMMSS.csv
└── tsg_backups/
    ├── TSG_gamma_1.0_YYYYMMDD_HHMMSS.txt
    ├── TSG_gamma_10.0_YYYYMMDD_HHMMSS.txt
    └── ...
```

### 2. Data Formats

```json
{
  "experiment_name": "gamma_analysis_20250706_003437",
  "timestamp": "20250706_003437",
  "config": {
    "gamma_values": [1.0, 10.0, 50.0, 100.0, 200.0, 400.0, 800.0],
    "output_formats": ["png", "pdf"],
    "chart_style": "professional"
  },
  "results": [
    {
      "gamma": 1.0,
      "edge_source": 81,
      "edge_dest": 82,
      "flow_value": 0,
      "gamma_cost": 200,
      "penalty_cost": 0,
      "has_violation": false,
      "violations_count": 0,
      "simulation_time": 1.2345,
      "status": "success"
    }
  ]
}
```

---

## 🚀 USAGE EXAMPLES

### 1. Demo Mode Examples

```bash
# Basic demo với default escape edge 81→82
python3 master_gamma_analysis.py --demo

# Demo với gamma values tùy chỉnh
python3 master_gamma_analysis.py --demo --gamma-values 1,5,10,20,50

# Demo với escape edge khác
python3 master_gamma_analysis.py --demo --escape-edge 75 80

# Demo với output directory tùy chỉnh
python3 master_gamma_analysis.py --demo --output-dir results --experiment-name test_gamma
```

### 2. Real Mode Examples

```bash
# Real simulation với default (TSG.txt, escape edge 81→82)
python3 master_gamma_analysis.py --real

# Real simulation với gamma values giới hạn
python3 master_gamma_analysis.py --real --gamma-values 1,10,50

# Real simulation với escape edge khác
python3 master_gamma_analysis.py --real --escape-edge 75 80

# Real simulation với DIMACS file tùy chỉnh
python3 master_gamma_analysis.py --real --dimacs-file my_tsg.txt --escape-edge 81 82
```

### 3. Advanced Usage

```bash
# Experiment với tên tùy chỉnh
python3 master_gamma_analysis.py --real --experiment-name "high_traffic_analysis" --output-dir production_results

# Phân tích với nhiều gamma values
python3 master_gamma_analysis.py --real --gamma-values 1,5,10,20,50,100,200,500

# Demo mode với nhiều test cases
python3 master_gamma_analysis.py --demo --gamma-values 0.1,0.5,1,2,5,10,25,50,100
```

### 4. Quick Testing

```bash
# Kiểm tra TSG.txt có escape edge 81→82 không
python3 master_gamma_analysis.py --real --gamma-values 1,200

# So sánh demo vs real
python3 master_gamma_analysis.py --demo --gamma-values 1,10,100 --experiment-name "demo_test"
python3 master_gamma_analysis.py --real --gamma-values 1,10,100 --experiment-name "real_test"
```

---

## 🐛 DEBUGGING & TROUBLESHOOTING

### 1. Common Issues

```
❌ COMMON PROBLEMS & SOLUTIONS:

1. "python command not found"
   → Solution: Use python3 instead of python

2. "'RestrictionForTimeFrameController' object has no attribute 'set_gamma_value'"
   → Solution: Updated - phương thức đã được thêm vào

3. "DIMACS file does not exist"
   → Solution: Tạo TSG file trước hoặc dùng --demo mode

4. "Real simulation modules not available"
   → Solution: Kiểm tra import paths và dependencies

5. "No violations detected"
   → Solution: Điều chỉnh restriction config để tạo violations
```

### 2. Debug Mode

```python
# Enable debug mode trong code
import pdb
pdb.set_trace()  # Breakpoint for debugging

# Verbose output
print(f"[DEBUG] Gamma value: {gamma_value}")
print(f"[DEBUG] Flow analysis: {flow_analysis}")
print(f"[DEBUG] Restrictions: {restrictions}")
```

---

## 🔮 FUTURE ENHANCEMENTS

### 1. Planned Features

```
🚀 ROADMAP:

1. Dynamic Gamma Control
   ├── Auto-adjusting gamma based on traffic load
   ├── Machine learning integration
   └── Real-time optimization

2. Multi-level Control
   ├── Different gamma values per restriction type
   ├── Hierarchical penalty structures
   └── Context-aware adjustments

3. Advanced Analytics
   ├── Predictive violation modeling
   ├── Performance optimization suggestions
   └── Cost-benefit optimization

4. Integration Improvements
   ├── Web dashboard interface
   ├── API endpoints for external tools
   └── Automated reporting system
```

### 2. Performance Optimizations

```
⚡ PERFORMANCE IMPROVEMENTS:

1. Parallel Processing
   ├── Multi-threaded gamma testing
   ├── Parallel chart generation
   └── Concurrent simulation runs

2. Memory Optimization
   ├── Streaming data processing
   ├── Efficient data structures
   └── Memory-mapped file handling

3. Caching System
   ├── Result caching for repeated tests
   ├── Intermediate computation caching
   └── Template-based report generation
```

---

## 📚 REFERENCES & RESOURCES

### 1. Technical Documentation

- **NetworkX Documentation**: Flow analysis algorithms
- **Matplotlib/Seaborn**: Professional visualization
- **DIMACS Format**: Network flow problem format
- **AGV Systems**: Automated Guided Vehicle principles

### 2. Related Files

- `controller/RestrictionForTimeFrameController.py`: Main restriction logic
- `gamma_analysis/integrated_gamma_control.py`: Gamma control integration
- `model/NXSolution.py`: Network flow solution handling
- `config.py`: System configuration parameters

---

*🎯 Master Gamma Analysis Tool v2.0 - Professional AGV System Analysis*

*📅 Last Updated: July 6, 2025*

*👨‍💻 Developed with ❤️ for AGV Traffic Management Research*
