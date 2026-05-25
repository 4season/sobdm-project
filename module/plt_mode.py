import numpy as np
import matplotlib.pyplot as plt


def plt_time_restored(y_test, y_pred, test_range):
    actual_angle = np.arctan2(y_test.iloc[:, 0], y_test.iloc[:, 1])
    actual_angle = np.where(actual_angle < 0, actual_angle + 2 * np.pi, actual_angle)
    cycle = 60
    actual_time = actual_angle * (cycle / (2 * np.pi))

    pred_angle = np.arctan2(y_pred[:, 0], y_pred[:, 1])
    pred_angle = np.where(pred_angle < 0, pred_angle + 2 * np.pi, pred_angle)
    pred_time = pred_angle * (cycle / (2 * np.pi))

    plt.figure(figsize=(12, 6))

    plt.scatter(range(test_range), actual_time[:test_range], label='Actual', color='blue', alpha=0.7)
    plt.scatter(range(test_range), pred_time[:test_range], label='Predicted', color='red', marker='x', s=60)

    plt.title(f'Comparison of First {test_range} Samples (Scatter View)')
    plt.ylabel('Restored Time Value')
    plt.xlabel('Sample Index (Randomly Shuffled)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    for i in range(test_range):
        plt.plot([i, i], [actual_time[i], pred_time[i]], color='gray', linestyle=':', alpha=0.5)

    plt.show()

def plt_hist_restored(history, cycle=60):
    train_mse = history.history['loss']
    val_mse = history.history['val_loss']

    epochs = range(1, len(train_mse) + 1)
    factor = (cycle / (2 * np.pi)) * 60

    train_error_sec = np.sqrt(train_mse) * factor
    val_error_sec = np.sqrt(val_mse) * factor

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_error_sec, label='Train Error (Approx. Seconds)')
    plt.plot(epochs, val_error_sec, label='Validation Error (Approx. Seconds)', linestyle='--')

    plt.title('Model Error in Seconds (Restored)')
    plt.ylabel('Error (Seconds)')
    plt.xlabel('Epochs')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    best_epoch = np.argmin(val_error_sec) + 1
    best_val_err = np.min(val_error_sec)
    plt.plot(best_epoch, best_val_err, 'ro', label=f'Best: {best_val_err:.2f} sec')
    plt.annotate(f'Epoch {best_epoch}\n{best_val_err:.1f}s',
                 (best_epoch, best_val_err),
                 xytext=(best_epoch + 1, best_val_err + 5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.show()