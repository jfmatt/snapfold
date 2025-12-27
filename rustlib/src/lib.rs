// Import the generated proto module
pub use gamedef_proto3::snapfold::gamedef::*;

/// A simple greeting function from the shared Rust library
pub fn get_greeting(name: &str) -> String {
    if name.is_empty() {
        "Hello from the Rust library!".to_string()
    } else {
        format!("Hello, {}! (from Rust library)", name)
    }
}

/// Creates a sample poker game structure
pub fn create_sample_game() -> GameStructure {
    GameStructure {
        id: "test-game".to_string(),
        name: "Test Texas Hold'em".to_string(),
        deck: Some(game_structure::Deck::StandardDeck(
            StandardDeck::DeckPoker.into(),
        )),
        phases: vec![
            Phase {
                phase_type: Some(phase::PhaseType::PlayerDeal(phase::PlayerDeal {
                    cards: 2,
                    face_up: false,
                })),
            },
            Phase {
                phase_type: Some(phase::PhaseType::BettingRound(phase::BettingRound {
                    name: "Pre-flop".to_string(),
                    min_bet: 1,
                    order: phase::betting_round::BettingOrder::FollowBlinds.into(),
                })),
            },
        ],
        community_board_count: 1,
        scorings: vec![],
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_greeting() {
        assert_eq!(get_greeting(""), "Hello from the Rust library!");
        assert_eq!(get_greeting("World"), "Hello, World! (from Rust library)");
    }

    #[test]
    fn test_proto_instantiation() {
        let game = create_sample_game();

        // Verify the proto message was created correctly
        assert_eq!(game.id, "test-game");
        assert_eq!(game.name, "Test Texas Hold'em");
        assert_eq!(game.phases.len(), 2);
        assert_eq!(game.community_board_count, 1);

        // Print the proto message (for debugging)
        println!("Created game structure: {:?}", game);

        // Verify the first phase is a player deal
        match &game.phases[0].phase_type {
            Some(phase::PhaseType::PlayerDeal(deal)) => {
                assert_eq!(deal.cards, 2);
                assert_eq!(deal.face_up, false);
            }
            _ => panic!("Expected PlayerDeal phase"),
        }

        // Verify the second phase is a betting round
        match &game.phases[1].phase_type {
            Some(phase::PhaseType::BettingRound(betting)) => {
                assert_eq!(betting.name, "Pre-flop");
                assert_eq!(betting.min_bet, 1);
            }
            _ => panic!("Expected BettingRound phase"),
        }
    }
}
