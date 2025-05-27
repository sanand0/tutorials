#!/usr/bin/env bash

echo "' AWS icon macros. They all accept (e_alias, e_label, e_techn). Prefer including AWSPuml/[CATEGORY]/all.puml" > AWS.puml
echo '!define AWSPuml https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/refs/heads/main/dist' >> AWS.puml
curl -s https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/refs/heads/main/AWSSymbols.md \
  | grep -Po '\b[\w./-]+\.puml\b' \
  | sed 's/^/!includeurl AWSPuml\//' \
  >> AWS.puml

echo "' Azure icon macros. They all accept (e_alias, e_label, e_techn). Prefer including AzurePuml/[CATEGORY]/all.puml. Always include AzurePuml/AzureCommon.puml
" > Azure.puml
echo '!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/master/dist' >> Azure.puml
curl -s https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/refs/heads/master/AzureSymbols.md \
  | grep -Po '\b[\w./-]+\.puml\b' \
  | grep -v 'AzurePuml/' \
  | sed 's/^/!includeurl AzurePuml\//' \
  >> Azure.puml

echo "' GCP icon macros. They all accept (e_alias, e_label, e_techn). Prefer including GCPPuml/[CATEGORY]/all.puml. Always include GCPPuml/GCPCommon.puml
" > GCP.puml
echo '!define GCPPuml https://raw.githubusercontent.com/Crashedmind/PlantUML-icons-GCP/refs/heads/master/dist' >> GCP.puml
curl -s https://raw.githubusercontent.com/Crashedmind/PlantUML-icons-GCP/refs/heads/master/Symbols.md \
  | grep -Po '\b[\w./-]+\.puml\b' \
  | sed 's/^/!includeurl GCPPuml\//' \
  >> GCP.puml
