% best = run_GA(50, 150, 0.6, 0.25);
% plot(1:GENERATIONS, best_of_all);

% change generation
% generation_sizes = [100 150 200];
% for i=1:length(generation_sizes)
%     G = generation_sizes(i);
%     best = run_GA(50, G, 0.6, 0.25);
%     subplot(3,1,i)
%     plot(1:G, best)
%     title(sprintf('Number of generations = %d',G))
% end

% change population size
% population_sizes = [30 50 100];
% for i=1:length(population_sizes)
%     P = population_sizes(i);
%     best = run_GA(P, 150, 0.6, 0.25);
%     subplot(3,1,i)
%     plot(1:150, best)
%     title(sprintf('Population size = %d',P))
% end

% change crossover p
% crossovers = [0.6 0.7 0.8];
% for i=1:length(crossovers)
%     C = crossovers(i);
%     best = run_GA(50, 150, C, 0.25);
%     subplot(3,1,i)
%     plot(1:150, best)
%     title(sprintf('Crossover probability = %0.1f',C))
% end

% change crossover p
mutations = [0.05 0.15 0.25];
for i=1:length(mutations)
    M = mutations(i);
    best = run_GA(50, 150, 0.6, M);
    subplot(3,1,i)
    plot(1:150, best)
    title(sprintf('Mutation probability = %0.2f',M))
end


function best_of_all = run_GA(POPULATION_SIZE, GENERATIONS, CROSSOVER_PROB, MUTATION_PROB)
    % Initialize population
    population = zeros(POPULATION_SIZE, 3);
    for i = 1:POPULATION_SIZE
        Kp = 2 + rand()*(18 - 2);
        Ti = 1.05 + rand()*(9.42 - 1.05);
        Td = 0.26 + rand()*(2.37 - 0.26);
        population(i, :) = [Kp Ti Td];
    end

    % Best fitness vector for each generation
    best_of_all = zeros(GENERATIONS, 1);
    best_population = [0 0 0];

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % main loop
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for g = 1:GENERATIONS
        fitness_values = get_fitness(population);
        parents = get_parents(population, fitness_values);
        offspring = crossover(parents, CROSSOVER_PROB);
        offspring = mutate(offspring, MUTATION_PROB);

        sorted_fitness = sort(fitness_values, 'descend');
        elite1 = find(fitness_values == sorted_fitness(1), 1);
        elite2 = find(fitness_values == sorted_fitness(2), 1);
        offspring(elite1,:) = population(elite1,:);
        offspring(elite2,:) = population(elite2,:);
        population = offspring;
        best_of_all(g) = sorted_fitness(1);
        best_population = population(elite1,:);
    end
    
    disp(best_population);

end


function fitness_values = get_fitness(population)
    N = length(population);
    fitness_values = zeros(N, 1);
    for i = 1:N
        [ISE, t_r, t_s, M_p] = perffcn(transpose(population(i,:)));
        fitness_values(i) = 1/sqrt(ISE);
    end
end

function parents = get_parents(population, fitness_values)
    N = length(population);
    parents = zeros(N, 3);
    total_fitness = sum(fitness_values);
    selected_weights = fitness_values/total_fitness;
     
    index_parents = randsample(1:N, N, true, selected_weights);
    for i = 1:N
        parents(i,:) = population(index_parents(i),:);
    end
end

function offspring = crossover(parents, CROSSOVER_PROB)
    alpha = 0.5;
    N = length(parents);
    offspring = zeros(N, 3);
    for i = 1:N/2
        parent1 = parents(i*2-1,:);
        parent2 = parents(i*2,:);
        if rand() < CROSSOVER_PROB
            child1 = parent1;
            child2 = parent2;
            k = randi(3);
            child1(k) = alpha * parent1(k) + (1-alpha) * parent2(k);
            child2(k) = alpha * parent2(k) + (1-alpha) * parent1(k);
            offspring(i*2-1,:) = child1;
            offspring(i*2,:) = child2;
        else
            offspring(i*2-1,:) = parent1;
            offspring(i*2,:) = parent2;
        end
    end
end

function offspring2 = mutate(offspring, MUTATION_PROB)
    N = length(offspring);
    offspring2 = offspring;
    for i = 1:N
        if rand() < MUTATION_PROB
            offspring2(i, 1) = 2 + rand()*(18 - 2);
        end
        if rand() < MUTATION_PROB
            offspring2(i, 2) = 1.05 + rand()*(9.42 - 1.05);
        end
        if rand() < MUTATION_PROB
            offspring2(i, 3) =  0.26 + rand()*(2.37 - 0.26);
        end
    end
end

