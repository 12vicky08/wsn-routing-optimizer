/*
 * IAGAPC-Enhanced: Enhanced Improved Adaptive Genetic Algorithm
 * for Mobile Sink Trajectory Optimization in Heterogeneous WSNs
 * Platform: Network Simulator 3 (NS-3)
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/energy-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <iostream>

using namespace ns3;

// -------------------------------------------------------------------------
// Simulation Parameters & Algorithm Constants
// -------------------------------------------------------------------------
const int POPULATION_SIZE = 50;
const int MAX_GENERATIONS = 200;
const int NUM_RPS = 10;          // Number of Rendezvous Points (Control Points)
const double V_MAX = 20.0;       // Maximum velocity of Mobile Sink (m/s)
const double COMM_RANGE = 100.0; // Communication range (m)

// Multi-Objective Weights
const double W_ENERGY = 0.4;     // Weight for Residual Energy Balance
const double W_SMOOTH = 0.3;     // Weight for Path Smoothness
const double W_COVERAGE = 0.2;   // Weight for Coverage/PDR
const double W_DELAY = 0.1;      // Weight for Delay/Path Length

// Adaptive Genetic Parameters
const double PC_MAX = 0.9;
const double PC_MIN = 0.6;
const double PM_MAX = 0.1;
const double PM_MIN = 0.01;

// Diversity Thresholds
const double DIVERSITY_CRIT = 25.0; // Threshold to trigger Cataclysm
const int STAGNATION_LIMIT = 20;

// -------------------------------------------------------------------------
// Data Structures
// -------------------------------------------------------------------------

struct Point {
    double x, y;
};

// Chromosome represents a potential trajectory solution
struct Chromosome {
    std::vector<Point> rps;        // Sequence of Rendezvous Points
    std::vector<double> dwellTimes; // Time spent at each RP
    double fitness;
    double diversityScore;
    
    // Evaluation Metrics
    double energyMetric;
    double smoothMetric;
    double coverageMetric;
    double delayMetric;

    Chromosome() : fitness(0.0), diversityScore(0.0) {}
};

// -------------------------------------------------------------------------
// IAGAPC-Enhanced Algorithm Class
// -------------------------------------------------------------------------

class IAGAPCEnhanced {
public:
    IAGAPCEnhanced(NodeContainer nodes, Ptr<EnergySourceContainer> energySources, double areaWidth, double areaHeight);
    void Run();
    std::vector<Point> GetBestTrajectory();
    double GetBestFitness();

private:
    NodeContainer m_nodes;
    Ptr<EnergySourceContainer> m_energySources;
    std::vector<Chromosome> m_population;
    double m_areaWidth;
    double m_areaHeight;
    Chromosome m_globalBest;

    // Initialization
    void InitializePopulation();
    
    // Core Genetic Operations
    void EvaluatePopulation();
    double CalculateFitness(Chromosome &ind);
    void Selection();
    void Crossover(const Chromosome &p1, const Chromosome &p2, Chromosome &c1, Chromosome &c2, double currentAvgFitness, double currentMaxFitness);
    void Mutation(Chromosome &ind, double currentDiversity);
    
    // Advanced Mechanisms
    void Cataclysm(); // Diversity reboot mechanism
    double CalculateDiversity();
    
    // Trajectory Helper Functions
    std::vector<Point> GenerateSplinePath(const std::vector<Point>& rps);
    double CalculateSmoothness(const std::vector<Point>& path);
    double CalculateResidualEnergyVariance();
};

// -------------------------------------------------------------------------
// Implementation
// -------------------------------------------------------------------------

IAGAPCEnhanced::IAGAPCEnhanced(NodeContainer nodes, Ptr<EnergySourceContainer> energySources, double w, double h) 
    : m_nodes(nodes), m_energySources(energySources), m_areaWidth(w), m_areaHeight(h) {
    InitializePopulation();
}

void IAGAPCEnhanced::InitializePopulation() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> disX(0, m_areaWidth);
    std::uniform_real_distribution<> disY(0, m_areaHeight);
    std::uniform_real_distribution<> disTime(5.0, 30.0);

    for (int i = 0; i < POPULATION_SIZE; ++i) {
        Chromosome ind;
        for (int j = 0; j < NUM_RPS; ++j) {
            ind.rps.push_back({disX(gen), disY(gen)});
            ind.dwellTimes.push_back(disTime(gen));
        }
        m_population.push_back(ind);
    }
}

// Catmull-Rom Spline Interpolation
// Converts discrete RPs into a smooth, kinematic-friendly path
std::vector<Point> IAGAPCEnhanced::GenerateSplinePath(const std::vector<Point>& rps) {
    std::vector<Point> splinePath;
    if (rps.size() < 4) return rps; 

    // Loop through control points
    for (size_t i = 0; i < rps.size() - 3; i++) {
        // Interpolate between p1 and p2 using p0 and p3 as control
        for (double t = 0; t <= 1; t += 0.05) {
            double t2 = t * t;
            double t3 = t2 * t;
            
            // Catmull-Rom Basis Matrix application
            double x = 0.5 * ((2 * rps[i+1].x) +
                       (-rps[i].x + rps[i+2].x) * t +
                       (2*rps[i].x - 5*rps[i+1].x + 4*rps[i+2].x - rps[i+3].x) * t2 +
                       (-rps[i].x + 3*rps[i+1].x - 3*rps[i+2].x + rps[i+3].x) * t3);
            
            double y = 0.5 * ((2 * rps[i+1].y) +
                       (-rps[i].y + rps[i+2].y) * t +
                       (2*rps[i].y - 5*rps[i+1].y + 4*rps[i+2].y - rps[i+3].y) * t2 +
                       (-rps[i].y + 3*rps[i+1].y - 3*rps[i+2].y + rps[i+3].y) * t3);
            
            splinePath.push_back({x, y});
        }
    }
    return splinePath;
}

// Evaluate smoothness based on curvature
double IAGAPCEnhanced::CalculateSmoothness(const std::vector<Point>& path) {
    double totalCurvature = 0.0;
    if (path.size() < 3) return 0.0;

    for (size_t i = 1; i < path.size() - 1; ++i) {
        // Calculate change in angle
        double dx1 = path[i].x - path[i-1].x;
        double dy1 = path[i].y - path[i-1].y;
        double dx2 = path[i+1].x - path[i].x;
        double dy2 = path[i+1].y - path[i].y;
        
        double angle1 = atan2(dy1, dx1);
        double angle2 = atan2(dy2, dx2);
        
        double diff = fabs(angle2 - angle1);
        // Penalize sharp turns heavily
        totalCurvature += (diff * diff);
    }
    
    // Normalize: Lower curvature -> Higher Score
    return 1.0 / (1.0 + (totalCurvature / path.size()));
}

// Multi-Objective Fitness Function
double IAGAPCEnhanced::CalculateFitness(Chromosome &ind) {
    std::vector<Point> smoothPath = GenerateSplinePath(ind.rps);
    
    // 1. Residual Energy Factor
    // In a real NS-3 sim, this would run a mini-simulation of data packet flow
    double minEnergy = 100.0; 
    double energyVar = 0.0;
    
    // Placeholder logic for energy extraction from NS-3 Energy Models
    // This assumes the trajectory was just "run" or estimated
    double sumEnergy = 0.0;
    for (uint32_t i = 0; i < m_nodes.GetN(); ++i) {
        double e = m_energySources->Get(i)->GetRemainingEnergy();
        if (e < minEnergy) minEnergy = e;
        sumEnergy += e;
    }
    double avgEnergy = sumEnergy / m_nodes.GetN();
    // Calculate Variance
    for (uint32_t i = 0; i < m_nodes.GetN(); ++i) {
         double e = m_energySources->Get(i)->GetRemainingEnergy();
         energyVar += pow(e - avgEnergy, 2);
    }
    energyVar /= m_nodes.GetN();
    
    ind.energyMetric = minEnergy / (sqrt(energyVar) + 1e-5); // Maximize MinEnergy, Minimize Var

    // 2. Smoothness Factor
    ind.smoothMetric = CalculateSmoothness(smoothPath);

    // 3. Delay Factor (Path Length)
    double pathLen = 0;
    for(size_t i=0; i<smoothPath.size()-1; ++i) {
        pathLen += std::hypot(smoothPath[i+1].x - smoothPath[i].x, 
                              smoothPath[i+1].y - smoothPath[i].y);
    }
    ind.delayMetric = 1.0 / (1.0 + (pathLen / V_MAX));

    // 4. Coverage Factor
    // Check how many nodes are within COMM_RANGE of at least one point on the path
    int coveredNodes = 0;
    for (uint32_t i = 0; i < m_nodes.GetN(); ++i) {
        Ptr<Node> n = m_nodes.Get(i);
        Ptr<MobilityModel> mob = n->GetObject<MobilityModel>();
        Vector pos = mob->GetPosition();
        
        bool isCovered = false;
        for (const auto& p : smoothPath) {
            if (std::hypot(pos.x - p.x, pos.y - p.y) <= COMM_RANGE) {
                isCovered = true;
                break;
            }
        }
        if (isCovered) coveredNodes++;
    }
    ind.coverageMetric = (double)coveredNodes / m_nodes.GetN();

    // Weighted Sum
    ind.fitness = (W_ENERGY * ind.energyMetric) + 
                  (W_SMOOTH * ind.smoothMetric) + 
                  (W_COVERAGE * ind.coverageMetric) + 
                  (W_DELAY * ind.delayMetric);
                  
    return ind.fitness;
}

// Diversity Calculation (Average Euclidean distance between all pairs)
double IAGAPCEnhanced::CalculateDiversity() {
    double totalDist = 0;
    int count = 0;
    for(size_t i=0; i<m_population.size(); ++i) {
        for(size_t j=i+1; j<m_population.size(); ++j) {
            double dist = 0;
            for(size_t k=0; k<NUM_RPS; ++k) {
                dist += std::hypot(m_population[i].rps[k].x - m_population[j].rps[k].x,
                                   m_population[i].rps[k].y - m_population[j].rps[k].y);
            }
            totalDist += dist;
            count++;
        }
    }
    return (count > 0)? totalDist / count : 0.0;
}

// The "Cataclysm" Operator: Resets population if diversity is too low
void IAGAPCEnhanced::Cataclysm() {
    double diversity = CalculateDiversity();
    
    if (diversity < DIVERSITY_CRIT) {
        NS_LOG_UNCOND("Cataclysm Triggered! Diversity: " << diversity);
        
        // Sort by fitness descending
        std::sort(m_population.begin(), m_population.end(), 
          (const Chromosome& a, const Chromosome& b) { return a.fitness > b.fitness; });
        
        // Elitism: Keep top 5%
        int eliteCount = (int)(POPULATION_SIZE * 0.05);
        
        // Regenerate the rest
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<> disX(0, m_areaWidth);
        std::uniform_real_distribution<> disY(0, m_areaHeight);
        
        for (int i = eliteCount; i < POPULATION_SIZE; ++i) {
             for (int j = 0; j < NUM_RPS; ++j) {
                m_population[i].rps[j] = {disX(gen), disY(gen)};
            }
            // Reset fitness
            m_population[i].fitness = 0.0;
        }
    }
}

// Adaptive Crossover
void IAGAPCEnhanced::Crossover(const Chromosome &p1, const Chromosome &p2, Chromosome &c1, Chromosome &c2, double f_avg, double f_max) {
    double f_prime = std::max(p1.fitness, p2.fitness);
    double Pc;
    
    // Adaptive Pc Formula
    if (f_prime >= f_avg) {
        Pc = PC_MAX * (f_max - f_prime) / (f_max - f_avg + 1e-5);
    } else {
        Pc = PC_MAX;
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    if (dis(gen) < Pc) {
        // Arithmetic Crossover
        double alpha = dis(gen);
        for (int i = 0; i < NUM_RPS; ++i) {
            c1.rps[i].x = alpha * p1.rps[i].x + (1 - alpha) * p2.rps[i].x;
            c1.rps[i].y = alpha * p1.rps[i].y + (1 - alpha) * p2.rps[i].y;
            c2.rps[i].x = alpha * p2.rps[i].x + (1 - alpha) * p1.rps[i].x;
            c2.rps[i].y = alpha * p2.rps[i].y + (1 - alpha) * p1.rps[i].y;
        }
    } else {
        c1 = p1;
        c2 = p2;
    }
}

// Main Loop
void IAGAPCEnhanced::Run() {
    for (int gen = 0; gen < MAX_GENERATIONS; ++gen) {
        
        // 1. Evaluate
        double maxFit = -1.0;
        double sumFit = 0.0;
        EvaluatePopulation();
        
        for(auto& ind : m_population) {
            if(ind.fitness > maxFit) maxFit = ind.fitness;
            sumFit += ind.fitness;
        }
        double avgFit = sumFit / POPULATION_SIZE;

        // 2. Cataclysm Check
        Cataclysm();

        // 3. Selection & Reproduction
        std::vector<Chromosome> newPop;
        
        // Elitism
        std::sort(m_population.begin(), m_population.end(), 
          (const Chromosome& a, const Chromosome& b) { return a.fitness > b.fitness; });
        newPop.push_back(m_population); // Keep best
        
        // Genetic Op Loop
        while(newPop.size() < POPULATION_SIZE) {
            // Tournament Selection
            int idx1 = rand() % POPULATION_SIZE;
            int idx2 = rand() % POPULATION_SIZE;
            Chromosome p1 = (m_population[idx1].fitness > m_population[idx2].fitness)? m_population[idx1] : m_population[idx2];
            
            idx1 = rand() % POPULATION_SIZE;
            idx2 = rand() % POPULATION_SIZE;
            Chromosome p2 = (m_population[idx1].fitness > m_population[idx2].fitness)? m_population[idx1] : m_population[idx2];
            
            Chromosome c1, c2;
            Crossover(p1, p2, c1, c2, avgFit, maxFit);
            
            double diversity = CalculateDiversity();
            Mutation(c1, diversity);
            Mutation(c2, diversity);
            
            newPop.push_back(c1);
            if(newPop.size() < POPULATION_SIZE) newPop.push_back(c2);
        }
        
        m_population = newPop;
        
        if (gen % 10 == 0) {
            NS_LOG_UNCOND("Generation " << gen << " Best Fitness: " << maxFit);
        }
    }
}

void IAGAPCEnhanced::Mutation(Chromosome &ind, double diversity) {
    // Adaptive Pm: Higher mutation when diversity is low
    double Pm = PM_MIN + (PM_MAX - PM_MIN) * exp(-0.1 * diversity);
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    std::normal_distribution<> gauss(0.0, 10.0); // Gaussian mutation

    for (int i = 0; i < NUM_RPS; ++i) {
        if (dis(gen) < Pm) {
            ind.rps[i].x += gauss(gen);
            ind.rps[i].y += gauss(gen);
            
            // Bounds check
            ind.rps[i].x = std::max(0.0, std::min(m_areaWidth, ind.rps[i].x));
            ind.rps[i].y = std::max(0.0, std::min(m_areaHeight, ind.rps[i].y));
        }
    }
}