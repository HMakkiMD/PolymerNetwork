clc; clear; close all;
maxNumCompThreads(15); % Set MATLAB to use 4 threads
tic
filename_input ='loop43.xlsx';
[~, ~, raw] = xlsread(filename_input);
bonds = str2double(raw);

% Graph
ibonds = size(bonds, 1);
jbonds = size(bonds, 2);

source_nodes = bonds(:, 1);
target_nodes = bonds(:, 2);

Z = zeros(ibonds, 1);
for i = 1:ibonds
   Z(i) = 1;     
end

edge = Z;

G = graph(source_nodes, target_nodes, edge);

% highlight nodes
% Load node IDs for categorization
acr_nodeIDs = xlsread('material-index-acr.xlsx');
mel_nodeIDs = xlsread('material-index-mel.xlsx');

% Separate edges connecting ACR nodes and HMMM nodes
acr_edges = [];
hmm_edges = [];

% Loop through each edge and categorize
for i = 1:ibonds
    if ismember(source_nodes(i), acr_nodeIDs) && ismember(target_nodes(i), acr_nodeIDs)
        acr_edges = [acr_edges; source_nodes(i), target_nodes(i)];
    elseif ismember(source_nodes(i), mel_nodeIDs) && ismember(target_nodes(i), mel_nodeIDs)
        hmm_edges = [hmm_edges; source_nodes(i), target_nodes(i)];
    end
end

% Plot the graph without node highlighting
h = plot(G, 'Layout', 'force');

% Highlight ACR edges in blue
for i = 1:size(acr_edges, 1)
    highlight(h, acr_edges(i, 1), acr_edges(i, 2), 'EdgeColor', [87/255, 199/255, 133/255], 'LineWidth', 2);
end

% Highlight HMMM edges in red
for i = 1:size(hmm_edges, 1)
    highlight(h, hmm_edges(i, 1), hmm_edges(i, 2), 'EdgeColor', [255/255, 190/255, 0/255], 'LineWidth', 2);
end

% Remove node markers completely
set(h, 'NodeColor', 'none');  % Set NodeColor to 'none' to remove node visibility

% Display results
disp('ACR Edges:');
disp(acr_edges);
disp('HMMM Edges:');
disp(hmm_edges);

toc