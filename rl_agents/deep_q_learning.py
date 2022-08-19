from agents.agent_interface import Agent
from environment import Game
from tensorflow import keras
from keras import layers
import tensorflow as tf
import numpy as np
import random


class DeepQLearningAgent(Agent):
    def __init__(self, name = 'DeepQLearningAgent', load_model_path: str = None, save_model_path: str = '.'):
        self.name = name
        self.save_model_path = save_model_path
        self.loaded_model = tf.keras.models.load_model(load_model_path) if load_model_path != None else None

    def decide(self, game_state, options):
        # print(f'Called decide in {self.name}.')
        if self.loaded_model != None:
            # print('Self decision took.')
            state = np.array(self.parse_game_state(game_state))
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = self.loaded_model(state_tensor, training=False)
            # Take best valid action. Of all the probs, get the valids one and then from them, the max one. So it gets the best valid option.
            max_valid_action_prob = (-1, min(action_probs[0]))
            for option in options:
                # print(option)
                for i, prob in enumerate(action_probs[0]):
                    # print(i, prob)
                    if option[0] == i and prob > max_valid_action_prob[1]:
                        max_valid_action_prob = (i, prob)
            action = max_valid_action_prob[0]
            # print(f'Selected {action} from {options} where probs: {action_probs[0]}')
        else:
            # print('Random decision took.')
            action = options[random.randint(0, len(options)-1)][0] if len(options) > 0 else None
            # print(f'Model {self.name} took random action: {action}.')    
        # print(f'Decition made by {self.name}: {action}.')
        return action

    def create_q_model(self, input_vector_size, output_vector_size, optimizer, loss_function):
        # Neural Network Arquitecture
        # The input shape is [1 2 3 4 5 6 7 1 2 3 4 5 6 7 4] (size = 15) --> (16^14)*4 = 288.230.376.151.711.744 total combinations (too many)
        # The input shape is [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 4] (size = 15) --> (2^30)*4 = 4.294.967.296 total combinations
        inputs = layers.Input(shape=(input_vector_size))

        # Hidden layers
        layer1 = layers.Dense(512, activation="relu")(inputs)
        layer2 = layers.Dense(256, activation="relu")(layer1)
        layer3 = layers.Dense(128, activation="relu")(layer2)
        layer4 = layers.Flatten()(layer3) 

        # Output layer
        output = layers.Dense(output_vector_size, activation="linear")(layer4)

        model = keras.Model(inputs=inputs, outputs=output)
        model.compile(optimizer=optimizer, loss=loss_function)

        return model if self.loaded_model == None else self.loaded_model

    def parse_game_state(self, game_state: dict):
        current_player_token_color = game_state['token_color']
        rival_player_token_color = 'dark' if current_player_token_color == 'light' else 'light'
        current_player_token_positions = [game_state[f'{current_player_token_color}_token_{token}_position'] for token in range(1,8)]
        rival_player_token_positions = [game_state[f'{rival_player_token_color}_token_{token}_position'] for token in range(1,8)]
        return current_player_token_positions + rival_player_token_positions + [game_state['dice_roll_result']]

    def parse_game_state_binary(self, game_state: dict):
        parsed_game_state = self.parse_game_state(game_state)
        return [1 if i in parsed_game_state[:7] else 0 for i in range(15)] + [1 if i in parsed_game_state[7:14] else 0 for i in range(15)] + [parsed_game_state[-1]]

    def get_reward(self, game_state: dict, action: int, options: tuple):
        try:
            option = tuple(filter(lambda x: x[0] == action, options))[0]
            dice_roll_probabilities = [(0, 0.0625), (1, 0.25), (2, 0.375), (3, 0.25), (4, 0.0625)]
            current_player_token_color = game_state['token_color']
            rival_player_token_color = 'dark' if current_player_token_color == 'light' else 'light'
            rival_player_token_positions = [game_state[f'{rival_player_token_color}_token_{token}_position'] for token in range(1,8)]
            next_turn_score_if_token_land_in_rossete_tile = ((1 + (option[1] + 1 if option[1] + 1 in rival_player_token_positions and option[1] + 1 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[1][1] + (2 + (option[1] + 2 if option[1] + 2 in rival_player_token_positions and option[1] + 2 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[2][1] + (3 + (option[1] + 3 if option[1] + 3 in rival_player_token_positions and option[1] + 3 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[3][1] + (4 + (option[1] + 4 if option[1] + 4 in rival_player_token_positions and option[1] + 4 in [5, 6, 7, 9, 10, 11, 12] else 0)) * dice_roll_probabilities[4][1]) if option[1] in [4, 8, 14] else 0
            return game_state['dice_roll_result'] + (option[1] if option[1] in rival_player_token_positions and option[1] in [5, 6, 7, 9, 10, 11, 12] else 0) + next_turn_score_if_token_land_in_rossete_tile, True
        except:
            return -100, False

    def train_model(self, initial_rival_model_path: str = None):
        # print('Loading training parameters...')
        # Training paramaters
        gamma = 0.99  # Discount factor for past rewards
        epsilon = 1.0  # Epsilon greedy parameter
        epsilon_min = 0.1  # Minimum epsilon greedy parameter
        epsilon_decay_value = 0.997  # Rate at which to reduce chance of random action being taken
        batch_size = 10  # Size of batch taken from replay buffer to update model
        input_vector_size = 15 # [1 2 3 4 5 6 7] [1 2 3 4 5 6 7] [4] own token positions, rival token positions and dice roll result 
        num_actions = 15 # from 0 to 14. Maximum number of actions the agent is able to make. One for each posible token position in the game. Except 15 that cant be moved.
        training_games_log_path = 'game_simulation_logs/training_games_logs'

        # Experience replay buffers
        action_history = []
        state_history = []
        state_next_history = []
        rewards_history = []
        games_count_history = []
        cumulative_game_reward_history = []
        steps_count = 0
        games_count = 0
        # Maximum replay length
        # Note: The Deepmind paper suggests 1000000 however this causes memory issues
        max_memory_length = 100000
        # Train the model after X games
        update_after_games = 1
        # Max games to train
        finish_after_games_count = 1000
        # How often to update the target network (after x games)
        update_target_network = 1
        # How often to save the model to a pickle file
        save_model_every_games_count = 1

        # Models creation
        # Adam optimizer improves training time
        optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
        # Using huber loss for stability
        loss_function = keras.losses.Huber()
        # print('Creating models...')
        # The first model makes the predictions for Q-values which are used to make a action.
        model = self.create_q_model(input_vector_size, num_actions, optimizer, loss_function)
        # Build a target model for the prediction of future rewards.
        # The weights of a target model get updated every certain number of steps or games thus, when the
        # loss between the Q-values is calculated, the target Q-value is stable.
        model_target = self.create_q_model(input_vector_size, num_actions, optimizer, loss_function)

        # Training loop
        while games_count < finish_after_games_count:  # Runs until X games played
            # print('Train loop started')
            # print(f'Games count: {games_count}.')
            # Loading rival model
            if games_count == 0 and initial_rival_model_path != None:
                rival_model = DeepQLearningAgent('DeepQLearningAgent2', load_model_path=initial_rival_model_path)
                # print(f'Initial rival model loaded: {initial_rival_model_path}')
            if games_count == 0 and initial_rival_model_path == None:
                rival_model = DeepQLearningAgent('DeepQLearningAgent2')
            if games_count != 0 and games_count % save_model_every_games_count == 0:
                rival_model = DeepQLearningAgent('DeepQLearningAgent2', load_model_path=f'{self.save_model_path}/{self.name}_{environment.game_state["game_id"]}_trained_for_{games_count}_games')
                print(f'New rival: {self.save_model_path}/{self.name}_{environment.game_state["game_id"]}_trained_for_{games_count}_games')
            # Create game environment
            # print('Creating game environment...')
            environment = Game(player1=Agent(self.name), player2=rival_model, log_path=training_games_log_path, auto_start_game_engine=False)
            games_count += 1
            # Decay probability of taking random action
            epsilon = max(epsilon*epsilon_decay_value, epsilon_min)

            while environment.is_game_finished() == False:
                options = environment.get_options() # get options player can play

                if environment.game_state['turn'] == self.name: # if it is your turn then play, if not, play the rival
                    if len(options) <= 1:
                        # print('Less than 2 options.')
                        # If there are no options (dice roll == 0) return None.
                        # If only 1 option, choose the only option available and do not ask the model
                        action = None if len(options) == 0 else options[0][0] 
                        environment.next_turn(action, options) # call next turn passing the option decision

                    # If there are more than 1 options to take, ask the model for a decision
                    if len(options) > 1:
                        state = np.array(self.parse_game_state(environment.game_state))
                        cumulative_game_reward = 0
                        steps_count += 1

                        # Use epsilon-greedy for exploration
                        print(f'Current epsilon: {epsilon}')
                        if epsilon >= np.random.rand(1)[0]:
                            # Take random action
                            # print('Random action taken.')
                            action = np.random.choice(num_actions)
                        else:
                            # Predict action Q-values
                            # From environment state
                            # print('Asked action to the model.')
                            state_tensor = tf.convert_to_tensor(state)
                            state_tensor = tf.expand_dims(state_tensor, 0)
                            action_probs = model(state_tensor, training=False)
                            # print(f'action_probs: {action_probs[0]}')
                            # Take best action
                            action = tf.argmax(action_probs[0]).numpy()
                            # print(f'action: {action}')

                        # Get reward before applying action to environment. The reward function is known and can be calculated just knowing the move you are going to make.
                        # But it does not garantee the victory. Thats why the decisions on the model are not bases on the maximum reward.
                        # print(f'Options of the model {options}.')
                        # print(f'Action taken by the model {action}.')
                        reward, valid_action = self.get_reward(environment.game_state, action, options)
                        # print(f'reward: {reward}')
                        # Apply the sampled action in our environment
                        # Test a function to step forward in the environment to get the new state, the reward and the is finished variable
                        if valid_action:
                            # print('Valid action. Doing next step...')
                            environment.next_turn(action, options) # call next turn passing the option decision
                        state_next = np.array(self.parse_game_state(environment.game_state))
                        done = environment.is_game_finished()
                        # print(f'Game turn_id: {environment.game_state["turn_id"]}')
                        cumulative_game_reward += reward
                        # print('Saving cumulative reward...')
                        # Save actions and states in replay buffer
                        # print('Saving actions and states in replay buffer...')
                        action_history.append(action)
                        state_history.append(state)
                        state_next_history.append(state_next)
                        games_count_history.append(done)
                        rewards_history.append(reward)
                        cumulative_game_reward_history.append(cumulative_game_reward)
                        # print('Finished saving actions and states in replay buffer.')

                        # Update every X games or once batch size is over the specified value
                        # print(done == True)
                        # print(done)
                        # print(len(action_history) >= batch_size)
                        if (games_count % update_after_games == 0 and done == True) or len(action_history) >= batch_size:
                            # print(games_count % update_after_games == 0)
                            # print(len(action_history) >= batch_size)
                            # print('Updating model...')
                            # Get indices of samples for replay buffers by random
                            # Add a boolean to make random or not. Is could be better if the model understand the consecuent actions
                            indices = np.random.choice(range(len(games_count_history)), size=batch_size)

                            # Using list comprehension to sample from replay buffer
                            state_sample = np.array([state_history[i] for i in indices])
                            state_next_sample = np.array([state_next_history[i] for i in indices])
                            rewards_sample = [rewards_history[i] for i in indices]
                            action_sample = [action_history[i] for i in indices]
                            games_count_sample = tf.convert_to_tensor(
                                [float(games_count_history[i]) for i in indices]
                            )

                            # Build the updated Q-values for the sampled future states
                            # Use the target model for stability
                            future_q_values_by_model_target = model_target.predict(state_next_sample)
                            # Q value = reward + discount factor * expected future Q value
                            updated_q_values = rewards_sample + gamma * tf.reduce_max(
                                future_q_values_by_model_target, axis=1
                            )

                            # If final step set the last value to -1
                            updated_q_values = updated_q_values * (1 - games_count_sample) - games_count_sample

                            # Create a mask so we only calculate loss on the updated Q-values
                            masks = tf.one_hot(action_sample, num_actions)

                            with tf.GradientTape() as tape:
                                # Train the model on the states and updated Q-values
                                q_values = model(state_sample)

                                # Apply the masks to the Q-values to get the Q-value for action taken
                                q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                                # Calculate loss between new Q-value and old Q-value
                                loss = loss_function(updated_q_values, q_action)

                            # Backpropagation
                            grads = tape.gradient(loss, model.trainable_variables)
                            optimizer.apply_gradients(zip(grads, model.trainable_variables))

                            # Cleaning the batch data
                            # print('Cleaning batch history data')
                            del rewards_history[:]
                            del state_history[:]
                            del state_next_history[:]
                            del action_history[:]
                            del games_count_history[:]

                        # print('Checking if target network needs to be updated...')
                        if games_count % update_target_network == 0:
                            # print('Updating target network.')
                            # update the the target network with new weights
                            model_target.set_weights(model.get_weights())
                            # Log details
                            template = "running reward: {:.2f} at episode {}, games {} step {}"

                        # Limit the state and reward history
                        # print('Checking memory limit...')
                        if len(rewards_history) > max_memory_length:
                            # print('Memory limit reached. Dropping first stored values.')
                            del rewards_history[:1]
                            del state_history[:1]
                            del state_next_history[:1]
                            del action_history[:1]
                            del games_count_history[:1]
                else:
                    # print('Playing rival...')
                    if len(options) <= 1:
                        # print('Less than 2 options.')
                        # If there are no options (dice roll == 0) return None.
                        # If only 1 option, choose the only option available and do not ask the model
                        action = None if len(options) == 0 else options[0][0] 
                        environment.next_turn(action, options) # call next turn passing the option decision
                    # If there are more than 1 options to take, ask the model for a decision
                    if len(options) > 1:
                        environment.next_turn(environment.player2.decide(environment.game_state, options), options) # call the rival model to play his turn

                # environment.print_game(options)
                # print('Checking if game is done at the very end...')
                # Notify game completition on training
                if environment.is_game_finished() == True:
                    print(f'Game {games_count} finished.')

                    # Saving model
                    if games_count % save_model_every_games_count == 0:
                        model.save(f'{self.save_model_path}/{self.name}_{environment.game_state["game_id"]}_trained_for_{games_count}_games')
                        # print(f'Model saved to {self.save_model_path}/{self.name}_{environment.game_state["game_id"]}_trained_for_{games_count}_games')